from django.db import models
import math


class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='locations/', null=True, blank=True)
    image_url = models.URLField(blank=True, help_text="External image URL (alternative to upload)")
    hint = models.CharField(max_length=300, blank=True, help_text="Optional hint for this location")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return None


class GameSession(models.Model):
    nickname = models.CharField(max_length=50)
    total_score = models.IntegerField(default=0)
    rounds_played = models.IntegerField(default=0)
    total_rounds = models.IntegerField(default=5)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nickname} - {self.total_score} pts"

    def get_accuracy(self):
        max_possible = self.total_rounds * 5000
        if max_possible == 0:
            return 0
        return round((self.total_score / max_possible) * 100, 1)


class GameRound(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='rounds')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    guessed_lat = models.FloatField(null=True, blank=True)
    guessed_lng = models.FloatField(null=True, blank=True)
    distance_meters = models.FloatField(null=True, blank=True)
    score = models.IntegerField(default=0)
    round_number = models.IntegerField()
    completed = models.BooleanField(default=False)
    time_taken = models.IntegerField(default=0, help_text="Seconds taken")

    class Meta:
        ordering = ['round_number']

    def __str__(self):
        return f"Round {self.round_number} - {self.session.nickname}"

    @staticmethod
    def calculate_distance(lat1, lng1, lat2, lng2):
        """Haversine formula to calculate distance in meters."""
        R = 6371000  # Earth radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lng2 - lng1)
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    @staticmethod
    def calculate_score(distance_meters):
        """Score out of 5000 based on distance. Max at 0m, 0 at 1km+."""
        if distance_meters <= 0:
            return 5000
        max_dist = 1000  # 1km = 0 points
        if distance_meters >= max_dist:
            return 0
        score = round(5000 * (1 - distance_meters / max_dist))
        return max(0, score)
