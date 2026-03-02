import os

print("=" * 80)
print("📁 CREATING UPLOAD DIRECTORIES")
print("=" * 80)

directories = [
    'uploads/qualifications',
    'uploads/profiles',
    'uploads/events',
    'static/uploads/qualifications'
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"✅ Created: {directory}")

print("\n✅ All upload directories ready!")