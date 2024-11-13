from django.db import models
import csv


# Create your models here.
class Voter(models.Model):
  '''a Voter model definition to represent a registered voter'''

  # Basic Information
  last_name = models.TextField()
  first_name = models.TextField()
  
  # Address Information
  street_number = models.CharField(max_length=10)
  street_name = models.CharField(max_length=100)
  apartment_number = models.CharField(max_length=10)
  zip_code = models.CharField(max_length=10)
  
  # Date Information
  date_of_birth = models.DateField()
  date_of_registration = models.DateField()
  
  # Voting and Political Information
  party_affiliation = models.CharField(max_length=50)
  precinct_number = models.CharField(max_length=20)
  
  # Election Participation
  v20state = models.BooleanField(default=False)  # Participated in the 2020 state election
  v21town = models.BooleanField(default=False)   # Participated in the 2021 town election
  v21primary = models.BooleanField(default=False)  # Participated in the 2021 primary election
  v22general = models.BooleanField(default=False)  # Participated in the 2022 general election
  v23town = models.BooleanField(default=False)   # Participated in the 2023 town election
  
  # Voter Score
  voter_score = models.IntegerField()  # Calculated based on participation in past elections

  def __str__(self):
    '''Return a string representation of this model instance.'''
    return f'{self.first_name} {self.last_name} {self.zip_code}'
  
def load_data():
  '''Function to load data records from CSV file into Django model instances.'''
  filename = '/Users/keithyeung/Downloads/newton_voters.csv'
  f = open(filename)
  f.readline()

  with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            voter = Voter(
                last_name=row[1],
                first_name=row[2],
                street_number=int(row[3]),
                street_name=row[4],
                apartment_number=row[5],
                zip_code=int(row[6]),
                date_of_birth=row[7],
                date_of_registration=row[8],
                party_affiliation=row[9],
                precinct_number=row[10],
                v20state=row[11].strip().lower() == 'true',
                v21town=row[12].strip().lower() == 'true',
                v21primary=row[13].strip().lower() == 'true',
                v22general=row[14].strip().lower() == 'true',
                v23town=row[15].strip().lower() == 'true',
                voter_score=int(row[16])
            )

            voter.save()
            print(f'Created voter: {voter}')