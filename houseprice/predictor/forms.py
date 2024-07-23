from django import forms
from .models import ZipCode, Year

class PredictionForm(forms.Form):
    
    FIREPLACE = [
        (0, 'No'),
        (1, 'Yes')
    ]
    
    CITY_CHOICES = [
        (0, 'Atlanta'),
        (1, 'Austin'),
        (3, 'Charlotte'),
        (5, 'Chicago'),
        (4, 'Chattanooga'),
        (6, 'Cleveland'),
        (30, 'Philadelphia'),
        (29, 'Palm Coast'),
        (28, 'Other'),
        (27, 'Orlando'),
        (26, 'Ocala'),
        (25, 'New York'),
        (24, 'Nashville'),
        (23, 'Miami Beach'),
        (22, 'Miami'),
        (21, 'Memphis'),
        (20, 'Los Angeles'),
        (19, 'Las Vegas'),
        (18, 'Lakewood'),
        (17, 'Kissimmee'),
        (16, 'Jacksonville'),
        (15, 'Indianapolis'),
        (14, 'Houston'),
        (13, 'Fort Worth'),
        (12, 'Fort Lauderdale'),
        (11, 'El Paso'),
        (8, 'Denver'),
        (7, 'Dallas'),
        (9, 'Detroit'),
        (10, 'Durham'),
        (2, 'Brooklyn'),
        (31, 'Port Charlotte'),
        (32, 'Portland'),
        (33, 'Punta Gorda'),
        (34, 'Raleigh'),
        (35, 'Saint Petersburg'),
        (36, 'San Antonio'),
        (37, 'San Diego'),
        (38, 'Seattle'),
        (39, 'Tampa'),
        (40, 'Washington'),
    ]

    STATE_CHOICES = [
        (4, 'FL'),
        (17, 'TX'),
        (10, 'NC'),
        (1, 'CA'),
        (16, 'TN'),
        (12, 'NY'),
        (13, 'OH'),
        (18, 'WA'),
        (6, 'IL'),
        (11, 'NV'),
        (2, 'CO'),
        (19, 'other'),
        (5, 'GA'),
        (15, 'PA'),
        (9, 'MI'),
        (3, 'DC'),
        (0, 'AZ'),
        (7, 'IN'),
        (14, 'OR'),
        (8, 'MA'),
    ]

    
    STATUS_CHOICES = [
        (5, 'For Sale'),
        (0, 'Active'),
        (7, 'Other'),
        (8, 'Closed'),
        (6, 'Pending'),
        (2, 'New construction'),
        (9, 'Auction'),
        (1, 'Under Contract'),
        (4, 'Contingent'),
        (3, 'Coming Soon'),
    ]

    PRIVATE_POOL = [
        (0, 'No'),
        (1, 'Yes'),
    ]
    
    PROPERTY_TYPE = [
        (7, 'Single-Family Home'),
        (1, 'Condominium/Apartment'),
        (5, 'Other/Various Styles'),
        (8, 'Townhouse'),
        (4, 'Multi-Family Home'),
        (9, 'Traditional'),
        (2, 'Contemporary/Modern'),
        (3, 'Manufactured/Mobile Home'),
        (6,'Ranch'),
        (0, 'Colonial')
    ]
    
    REMODELED_YEAR = [
        (0, 'No'),
        (1, 'Yes'),
    ]
    
    HEATING_TYPE = [
        (0, 'air'),
        (4, 'no data'),
        (5, 'other'),
        (1, 'central'),
        (3, 'gas'),
        (2, 'electric'),
        (6, 'pump'),
    ]

    COOLING_TYPE = [
        (1, 'central'),
        (3, 'no data'),
        (4, 'other'),
        (0, 'air'),
        (2, 'gas'),
    ]

    PARKING = [
        (0, '0 lot'),
        (3, 'garage'),
        (4, 'other'),
        (2, '2 lots'),
        (1, '1 lot'),
    ]
    
    SCHOOL_DISTANCE = [
        (4, 'up to 0.5'),
        (0, '0.5 to 1'),
        (1, '1 to 2'),
        (2, '2 to 5'),
        (3, 'above 5'),
    ]

    SCHOOL_QUANTITY = [
        (0, '1'),
        (1, '2'),
        (2, '3'),
        (3, 'above 5'),
    ]

    STORIES_CHOICES = [
        (0, '1'),
        (1, '2'),
        (2, '3'),
        (3, '4'),
        (4, '5-10'),
        (5, 'above 10'),
    ]

    
    fireplace = forms.ChoiceField(choices=FIREPLACE)
    city = forms.ChoiceField(choices=CITY_CHOICES)
    # Query the database for zip code choices
    ZIPCODE_CHOICES = [(zipcode.id, zipcode.zipcode) for zipcode in ZipCode.objects.all()]
    zipcode = forms.ChoiceField(choices=sorted(ZIPCODE_CHOICES, key=lambda x: x[1]), label='Zip Code')
    
    state = forms.ChoiceField(choices=STATE_CHOICES)
    status_category = forms.ChoiceField(choices=STATUS_CHOICES)
    private_pool = forms.ChoiceField(choices=PRIVATE_POOL)
    property_type = forms.ChoiceField(choices=PROPERTY_TYPE)

    baths = forms.FloatField()
    beds = forms.FloatField()

    # Query the database for year choices
    YEAR_CHOICES = [(year.id, year.year_built) for year in Year.objects.all()]
    year = forms.ChoiceField(choices=sorted(YEAR_CHOICES, key=lambda x: x[1]), label='Year built')
    
    remodeled = forms.ChoiceField(choices=REMODELED_YEAR)
 
    heating = forms.ChoiceField(choices=HEATING_TYPE)
    cooling = forms.ChoiceField(choices=COOLING_TYPE)
    parking = forms.ChoiceField(choices=PARKING)
    lotsize = forms.IntegerField()
    
    school_distance = forms.ChoiceField(choices=SCHOOL_DISTANCE)
    school_quantity = forms.ChoiceField(choices=SCHOOL_QUANTITY)
    
    sqft = forms.FloatField()
    stories = forms.ChoiceField(choices=STORIES_CHOICES)