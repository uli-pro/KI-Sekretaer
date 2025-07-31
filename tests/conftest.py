"""
Test-Konfiguration für pytest
"""
import os
import tempfile
import pytest
from app import create_app, db
from app.models import User


@pytest.fixture(scope='session')
def app():
    """Create application for testing"""
    # Temporäre Datei für Test-Datenbank
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    
    # Aufräumen
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='function')
def client(app):
    """Test client for the app"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Test runner for CLI commands"""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def db_session(app):
    """Database session for tests"""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        
        # Configure session
        options = dict(bind=connection, binds={})
        session = db.create_scoped_session(options=options)
        
        # Make session available
        db.session = session
        
        yield session
        
        # Cleanup
        transaction.rollback()
        connection.close()
        session.remove()


@pytest.fixture
def auth_headers(client, test_user):
    """JWT Token für authentifizierte Requests"""
    response = client.post('/api/auth/login', json={
        'email': test_user.email,
        'password': 'testpass123'
    })
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def test_user(db_session):
    """Test User erstellen"""
    user = User(
        email='test@example.com',
        username='testuser',
        password='testpass123'
    )
    user.first_name = 'Test'
    user.last_name = 'User'
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_users(db_session):
    """Mehrere Test User erstellen"""
    users = []
    for i in range(3):
        user = User(
            email=f'test{i}@example.com',
            username=f'testuser{i}',
            password='testpass123'
        )
        db_session.add(user)
        users.append(user)
    db_session.commit()
    return users
