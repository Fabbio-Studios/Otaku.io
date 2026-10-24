from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Obra, Profile, SolicitacaoObra


class ObraDetailTests(TestCase):
    def test_missing_work_does_not_create_database_record(self):
        response = self.client.get(reverse('detalhes_obra', args=['obra-inexistente']))

        self.assertEqual(response.status_code, 404)
        self.assertFalse(Obra.objects.exists())

    def test_registration_creates_profile_with_required_name(self):
        response = self.client.post(reverse('register'), {
            'username': 'new-user',
            'email': 'new@example.com',
            'password': 'a-long-test-password-123',
            'password2': 'a-long-test-password-123',
        })

        self.assertRedirects(response, reverse('profile_photo'))
        self.assertEqual(User.objects.get(username='new-user').profile.name, 'new-user')


class ReadOnlyDeploymentTests(TestCase):
    @override_settings(READ_ONLY_MODE=True)
    def test_post_returns_service_unavailable_instead_of_writing(self):
        response = self.client.post(reverse('register'), {
            'username': 'new-user',
            'email': 'new@example.com',
            'password': 'a-long-test-password-123',
            'password2': 'a-long-test-password-123',
        })

        self.assertEqual(response.status_code, 503)
        self.assertContains(response, 'modo de leitura', status_code=503)
        self.assertFalse(User.objects.filter(username='new-user').exists())

    @override_settings(READ_ONLY_MODE=True)
    def test_legacy_get_delete_action_does_not_write(self):
        user = User.objects.create_user(username='reader', password='test-password')
        solicitacao = SolicitacaoObra.objects.create(
            usuario=user,
            titulo='Obra solicitada',
        )

        response = self.client.get(
            reverse('excluir_solicitacao', args=[solicitacao.id])
        )

        self.assertEqual(response.status_code, 503)
        self.assertTrue(SolicitacaoObra.objects.filter(id=solicitacao.id).exists())

    def test_upload_profile_get_does_not_create_profile(self):
        user = User.objects.create_user(username='reader', password='test-password')
        Profile.objects.filter(user=user).delete()
        self.client.force_login(user)

        response = self.client.get(reverse('profile_photo'))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Profile.objects.filter(user=user).exists())
