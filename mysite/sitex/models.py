from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser



roles = {'GuestRole': 'guest',
        'StaffRole': 'staff',
        'AdminRole': 'admin',
        }


class UserManager(BaseUserManager):

    def create_user(self, email, password, nickname):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.nickname = nickname
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, nickname):
        user = self.create_user(
            email,
            password,
            nickname,
        )
        user.admin = True
        user.role = roles['AdminRole']
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email, password, nickname):
        user = self.create_user(
            email,
            password,
            nickname,
        )
        user.admin = True
        user.role = roles['StaffRole']
        user.nickname = nickname
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    nickname = models.CharField(max_length=255, blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    role = models.CharField(default='guest')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        db_table = 'Users'
        managed = True
        
    
    objects = UserManager()

    def get_nickname(self):
        return self.nickname

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    def get_user_role(self):
        return self.role

    @property
    def is_admin(self):
        return self.role == roles['AdminRole']

    @property
    def is_staff(self):
        if self.role == roles['AdminRole']:
            return True
        return self.role == roles['StaffRole']


class UserLastCurrency(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currencyfrom = models.CharField(max_length=255)
    currencyto = models.CharField(max_length=255)
    amount = models.IntegerField()

    class Meta:
        db_table = 'Currency'
        managed = True
        verbose_name = 'Currency'

    def __str__(self):
        return f'{self.id} {self.userid}'
