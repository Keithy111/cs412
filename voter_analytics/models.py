from django.db import models

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
  voter_score = models.IntegerField(default=0)  # Calculated based on participation in past elections
  
  def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    filename = '/Users/keithyeung/Downloads/newton_voters.csv'
    f = open(filename)
    f.readline()

    for line in f:
      fields = line.split(',')

      try:
        voter = Voter(last_name=fields[0],
                first_name=fields[1],
                street_number=fields[2],
                street_name=fields[3],
                apartment_number=fields[4],
                zip_code=fields[5],
                
                date_of_birth=fields[6],
                date_of_registration=fields[7],
                
                party_affiliation=fields[8],
                precinct_number=fields[9],
                
                v20state=fields[10],
                v21town=fields[11],
                v21primary=fields[12],
                v22general=fields[13],
                v23town=fields[14],
                
                voter_score=fields[15])
        voter.save()
        print(f'Created result: {voter}')
      except:
        print(f"skipped: {fields}")
    print(f'Done. Created {len(Voter.objects.all())} Voters.')