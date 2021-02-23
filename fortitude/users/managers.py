from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, password):
        if not username:
            raise ValueError('The username must be set.')

        user = self.model(username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)

        user.is_active = True
        user.is_admin = True
        user.is_superuser = True

        user.save()

        return user
