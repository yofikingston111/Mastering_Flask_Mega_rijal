from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='lala')
        u.set_password('ads')
        self.assertFalse(u.check_password('asd'))
        self.assertTrue(u.check_password('ads'))

    def test_avatar(self):
        u = User(username='rijal', email='ortonrko90900@gmail.com')
        self.assertEqual(u.avatar(126), ('https://www.gravatar.com/avatar/'
                                         '4c0c8170127954222428ab072fd90428'
                                         '?d=identicon&s=126'))

    def test_follow(self):
        u2 = User(username='lala', email='lala@gmail.com')
        u3 = User(username='rijal', email='rijal@gmail.com')
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()
        self.assertEqual(u2.followed.all(), [])
        self.assertEqual(u2.followers.all(), [])

        u2.follow(u3)
        db.session.commit()
        self.assertTrue(u2.is_following(u3))
        self.assertEqual(u2.followed.count(), 1)
        self.assertEqual(u2.followed.first().username, 'rijal')
        self.assertEqual(u3.followers.count(), 1)
        self.assertEqual(u3.followers.first().username, 'lala')

        u2.unfollow(u3)
        db.session.commit()
        self.assertFalse(u2.is_following(u3))
        self.assertEqual(u2.followed.count(), 0)
        self.assertEqual(u3.followers.count(), 0)

    def test_follow_posts(self):
        # create four posts
        u2 = User(username='lala', email='lala@gmail.com')
        u3 = User(username='rijal', email='rijal@gmail.com')
        u4 = User(username='muklis', email='muklis@gmail.com')
        u5 = User(username='yesi', email='yesi@gmail.com')
        db.session.add_all([u2, u3, u4, u5])

        # create four post
        now = datetime.utcnow()
        p2 = Post(body="post from rijal", author=u2,
                  timestamp=now + timedelta(seconds=2))
        p3 = Post(body="post from lala", author=u3,
                  timestamp=now + timedelta(seconds=5))
        p4 = Post(body="post from muklis", author=u4,
                  timestamp=now + timedelta(seconds=4))
        p5 = Post(body="post from yesi", author=u5,
                  timestamp=now + timedelta(seconds=3))
        db.session.add_all([p2, p3, p4, p5])
        db.session.commit()

        # setup the followers
        u2.follow(u3) # lala follows rijal
        u2.follow(u5) # lala follows yesi
        u3.follow(u4) # rijal follows muklis
        u4.follow(u5) # muklis follows yesi

        # setup the followers posts of each user
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        f5 = u5.followed_posts().all()
        self.assertEqual(f2, [p3, p5, p2])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4, p5])
        self.assertEqual(f5, [p5])

if __name__ == '__main__':
    unittest.main(verbosity=2)

