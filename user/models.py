from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, \
    BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):
    """custom user management"""

    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('Users must provide phone number')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password):
        """Create a new super user"""
        user = self.create_user(phone, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=14, unique=True)
    referral = models.ForeignKey('self', default=None,
                                 on_delete=models.SET_NULL,
                                 null=True)
    birth_date = models.DateField(null=True)
    image = models.ImageField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.phone


class UserAddress(models.Model):
    """Model for managing users address"""
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=500)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} - {self.address}'


class UserScoreTransaction(models.Model):
    """Store and check the user scores transactions"""
    score_types = (('profile', 'profile'), ('referral', 'referral'))
    type_points = (('profile', 1), ('referral', 1))
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    types = models.CharField(max_length=255, choices=score_types)
    points = models.CharField(max_length=255, choices=type_points)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    @staticmethod
    def add_transactions(user_id, point_type):
        """Add an user score transaction based on type"""
        type_points_dict = dict(UserScoreTransaction.type_points)
        UserScoreTransaction.objects.create(user_id=user_id, types=point_type,
                                            points=type_points_dict[point_type])

        UserScore.update_or_create_score(user_id, point_type)

    def __str__(self):
        return f'{self.user.phone} get {self.points} score by {self.types}'


class UserScore(models.Model):
    """Store the user scores based on score type"""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    types = models.CharField(max_length=255, choices=UserScoreTransaction.score_types)
    points = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    @staticmethod
    def update_or_create_score(user_id, point_type):
        """Creates or updates the user total score based on score type"""
        type_points_dict = dict(UserScoreTransaction.type_points)
        query = UserScore.objects.filter(user_id=user_id).filter(types=point_type)
        if query:
            user_point = UserScore.objects.filter(user_id=user_id).filter(types=point_type).first().points
            query.update(points=user_point + type_points_dict[point_type])
        else:
            UserScore.objects.create(user_id=user_id, types=point_type, points=type_points_dict[point_type])

    def __str__(self):
        return f'{self.user.phone} has {self.points} scores'
