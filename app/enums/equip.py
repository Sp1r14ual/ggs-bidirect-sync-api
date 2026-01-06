from aenum import Enum

class BaseEnum(Enum):
    _init_ = 'value string'

    def __str__(self):
        return self.string

    @classmethod
    def _missing_value_(cls, value):
        for member in cls:
            if member.string == value:
                return member

class EquipType(BaseEnum):
    not_chosen = 0, None
    heating_boiler = 654, "Котел отопительный"
    convector = 655, "Конвектор"
    water_heater = 656, "Водонагреватель"
    indirect_heating_boiler = 657, "Бойлер косвенного нагрева"
    outdoor_gas_pipeline = 658, "Газопровод наружный"
    indoor_gas_pipeline = 947, "Газопровод внутренний"
    thermal_shut_off_valve = 659, "Клапан термозапорный"
    gas_tap = 660, "Кран газовый"
    solenoid_valve = 661, "Электромагнитный клапан"
    gas_filter = 662, "Фильтр газовый"
    dielectric_coupling = 663, "Диэлектрическая муфта"
    gas_meter = 664, "Счетчик газа"
    gas_stove = 665, "Плита газовая"
    hob = 666, "Варочная панель"
    gas_detector = 667, "Сигнализатор загазованности"

class PackingType(BaseEnum):
    not_chosen = 0, None
    underground = 683, "Подземный"
    aboveground = 682, "Надземный"

class MarkType(BaseEnum):
    not_chosen = 0, None
    ACV = 1920, 'ACV'
    AEG = 1921, 'AEG'
    Arderia = 1922, 'Arderia'
    Ariston = 1923, 'Ariston'
    BaltGaz = 1924, 'BaltGaz'
    Baltur = 1925, 'Baltur'
    Baxi = 1926, 'Baxi'
    Beretta = 1927, 'Beretta'
    Biasi = 1928, 'Biasi'
    Bosch = 1929, 'Bosch'
    Buderus = 1930, 'Buderus'
    Celtic = 1931, 'Celtic'
    Chaffotealux = 1932, 'Chaffotealux'
    Daesung = 1933, 'Daesung'
    Daewoo = 1934, 'Daewoo'
    De_Dietrich = 1935, 'De Dietrich'
    Electrolux = 1936, 'Electrolux'
    Federica_Bugatti = 1937, 'Federica Bugatti'
    Ferroli = 1938, 'Ferroli'
    Fondital = 1939, 'Fondital'
    Gassero = 1940, 'Gassero'
    Habitat = 1941, 'Habitat'
    Haier = 1942, 'Haier'
    Hermann = 1943, 'Hermann'
    Hydrosta = 1944, 'Hydrosta'
    Immergas = 1945, 'Immergas'
    ITALTHERM = 1946, 'ITALTHERM'
    Junkers = 1947, 'Junkers'
    Kentatsu = 1948, 'Kentatsu'
    Kiturami = 1949, 'Kiturami'
    Lamborghini = 1950, 'Lamborghini'
    Master_Gas = 1951, 'Master Gas'
    Meteor = 1952, 'Meteor'
    Mizudo = 1953, 'Mizudo'
    Monlan = 1954, 'Monlan'
    Motan = 1955, 'Motan'
    Navien = 1956, 'Navien'
    NevaLux = 1957, 'NevaLux'
    Oasis = 1958, 'Oasis'
    Olympia = 1959, 'Olympia'
    Polykraft = 1960, 'Polykraft'
    Protherm = 1961, 'Protherm'
    Riello = 1962, 'Riello'
    Rinnai = 1963, 'Rinnai'
    Rocterm = 1964, 'Rocterm'
    RODA = 1965, 'RODA'
    Rossen = 1966, 'Rossen'
    Royal_Thermo = 1967, 'Royal Thermo'
    Sigma = 1968, 'Sigma'
    Sime = 1969, 'Sime'
    Termica = 1970, 'Termica'
    Therm = 1971, 'Therm'
    Thermex = 1972, 'Thermex'
    Thermona = 1973, 'Thermona'
    Unical = 1974, 'Unical'
    Vaillant = 1975, 'Vaillant'
    Viessmann = 1976, 'Viessmann'
    WARM = 1977, 'WARM'
    Wiesberg = 1978, 'Wiesberg'
    Wolf = 1979, 'Wolf'

class DuType(BaseEnum):
    zero = 0, None
    fifteen = 1980, 15
    twenty = 1981, 20
    twenty_five = 1982, 25
    thirty_two = 1983, 32
    forty = 1984, 40
    fifty = 1985, 50
    sixty_five = 1986, 65
    eighty = 1987, 80
    one_hundred = 1988, 100
    one_hundred_ten = 1989, 110

class DiameterType(BaseEnum):
    zero = 0, None
    fifteen = 897, 15
    # Добавить остальные диаметры, если появятся

class StoveType(BaseEnum):
    zero = 0, None
    pg_one = 694, 1
    pg_two = 695, 2
    pg_three = 696, 3
    pg_four = 697, 4
    pg_five = 698, 5
    pg_six = 699, 6
    pg_seven = 700, 7
    pg_eight = 701, 8
    pg_nine = 702, 9
    pg_ten = 703, 10


class PipeMaterialType(BaseEnum):
    not_chosen = 0, None
    polyethylene = 685, "Полиэтилен"
    metal = 684, "Металл"

class BoilSetupType(BaseEnum):
    not_chosen = 0, None
    wall = 668, "Настенный"
    floor = 669, "Напольный"
    parapetny = 670, "Парапетный"














    