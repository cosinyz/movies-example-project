from rest_framework import status
from rest_framework.test import APITestCase

from .models import Movie


class MovieApiTests(APITestCase):
    def setUp(self):
        Movie.objects.all().delete()
        self.low_rated = Movie.objects.create(
            title='A Film',
            description='',
            year=2000,
            rating='7.9',
        )
        self.top_rated = Movie.objects.create(
            title='Top Film',
            description='',
            year=2001,
            rating='9.2',
        )
        self.threshold_movie = Movie.objects.create(
            title='Threshold Film',
            description='',
            year=2002,
            rating='8.0',
        )

    def test_top_movies_only_includes_rating_of_eight_or_higher_in_descending_order(self):
        response = self.client.get('/api/movies/top/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [movie['id'] for movie in response.data],
            [self.top_rated.id, self.threshold_movie.id],
        )

    def test_movie_list_and_create(self):
        list_response = self.client.get('/api/movies/')
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 3)

        create_response = self.client.post(
            '/api/movies/',
            {
                'title': 'New Film',
                'description': 'A new film.',
                'year': 2024,
                'rating': '8.5',
            },
            format='json',
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data['title'], 'New Film')

    def test_movie_detail_and_delete(self):
        detail_response = self.client.get(f'/api/movies/{self.top_rated.id}/')
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data['title'], 'Top Film')

        delete_response = self.client.delete(f'/api/movies/{self.top_rated.id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movie.objects.filter(pk=self.top_rated.id).exists())
