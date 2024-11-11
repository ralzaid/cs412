from django.db import models
from django.db import models

class Voter(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50) 
    street_number = models.CharField(max_length=10) 
    street_name = models.CharField(max_length=100)  
    apartment_number = models.CharField(max_length=10)  
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)

    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"



from .models import Voter

def load_data():
    filename = 'Users/rafu/Downloads/newton_voters.csv'
    f = open(filename)
    f.readline()
    
    for _ in range(5):
        line = f.readline().strip()
        fields = line.split(',')
        
        voter = Voter(
            last_name=fields[0],
            first_name=fields[1],
            street_number=fields[2],
            street_name=fields[3],
            apartment_number=fields[4],
            zip_code=fields[5],
            date_of_birth=fields[6],
            date_of_registration=fields[7],
            party_affiliation=fields[8],
            precinct_number=fields[9],
            
            v20state=fields[10] == '1',
            v21town=fields[11] == '1',
            v21primary=fields[12] == '1',
            v22general=fields[13] == '1',
            v23town=fields[14] == '1',

            voter_score=sum(int(fields[i] == '1') for i in range(10, 15))

        )
        
        print(f'Created voter: {voter}')
