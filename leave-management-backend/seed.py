from app import create_app, db
from app.models import User

def seed_database():
    app = create_app()
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        admin_user = User(
            name='Admin User',
            email='admin@company.com',
            role='admin'
        )
        admin_user.set_password('admin123')
        
        employee1 = User(
            name='John Doe',
            email='john@company.com',
            role='employee'
        )
        employee1.set_password('password123')
        
        employee2 = User(
            name='Jane Smith',
            email='jane@company.com',
            role='employee'
        )
        employee2.set_password('password123')
        
        db.session.add(admin_user)
        db.session.add(employee1)
        db.session.add(employee2)
        db.session.commit()
        
        print("Database seeded successfully!")
        print("Admin credentials: admin@company.com / admin123")
        print("Employee credentials: john@company.com / password123")
        print("Employee credentials: jane@company.com / password123")

if __name__ == '__main__':
    seed_database()