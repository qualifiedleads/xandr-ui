import json

import xmltodict

from api.models import *


def create_carrier_extract(obj):
    site_id = obj['CarrierExtract']['SiteID']
    file_type = obj['CarrierExtract']['FileType']
    carrier_extract = CarrierExtract.objects.create(site_id=site_id, file_type=file_type)

    return carrier_extract


def create_driver_shift(obj, ce):
    driver_shift = DriverShift.objects.create(carrier_extract=ce)

    return driver_shift


def create_shift(shift_obj, ds):
    shift_id = shift_obj['ShiftID']
    start_location_id = shift_obj['StartLocationID']
    end_location_id = shift_obj['EndLocationID']
    driver_id = shift_obj['DriverID']
    driver_name = shift_obj['DriverName']
    shift_start_date_time = "%s %s" % (shift_obj['ShiftStartDate'], shift_obj['ShiftStartTime'])
    shift_end_date_time = "%s %s" % (shift_obj['ShiftEndDate'], shift_obj['ShiftEndTime'])

    start_location, created = Location.objects.get_or_create(code=start_location_id)
    end_location, created = Location.objects.get_or_create(code=end_location_id)

    shift = Shift.objects.create(driver_shift=ds, shift_id=shift_id, start_location_id=start_location,
                                 end_location_id=end_location, driver_id=driver_id, driver_name=driver_name,
                                 shift_start_date_time=shift_start_date_time, shift_end_date_time=shift_end_date_time)
    return shift


def create_shift_events(obj, shift):
    events = []

    shift_events = obj['ShiftEvents']['Events']
    for event in shift_events:
        ev = event

        event_code = ev['EventCode']
        event_code_description = ev['EventCodeDescription']
        event_start_date_time = "%s %s" % (ev['EventStartDate'], ev['EventStartTime'])
        event_end_date_time = "%s %s" % (ev['EventEndDate'], ev['EventEndTime'])

        shift_event = ShiftEvent.objects.create(shift=shift, event_code=event_code,
                                                event_code_description=event_code_description,
                                                event_start_date_time=event_start_date_time,
                                                event_end_date_time=event_end_date_time)

    return events


def create_loads(obj, shift):
    out = []

    loads = obj['Loads']['Load']
    for load_inst in loads:
        ld = load_inst

        load_id = ld['LoadID']
        resource_id = ld['ResourceID']
        resource_reference = ld['ResourceReference']
        trailer_id = ld['TrailerID']
        trailer_reference = ld['TrailerReference']
        start_location_id_1 = ld['StartLocationID1']
        end_location_id_1 = ld['EndLocationID1']
        load_depart_date_time = "%s %s" % (ld['LoadDepartDate'], ld['LoadDepartTime'])
        load_return_date_time = "%s %s" % (ld['LoadReturnDate'], ld['LoadReturnTime'])
        start_km = ld['StartKM']
        end_km = ld['EndKM']

        start_location_1, created = Location.objects.get_or_create(code=start_location_id_1)
        end_location_1, created = Location.objects.get_or_create(code=end_location_id_1)

        load = ShiftLoad.objects.create(shift=shift, load_id=load_id, resource_id=resource_id,
                                        resource_reference=resource_reference, trailer_id=trailer_id,
                                        trailer_reference=trailer_reference, start_location1=start_location_1,
                                        end_location1=end_location_1, load_depart_date_time=load_depart_date_time,
                                        load_return_date_time=load_return_date_time,
                                        start_km=start_km, end_km=end_km)

        ### Load can have many stops
        path = ld['Stops']['Stop']
        stops = create_stops(path, load)

        ### Each Load can have many load distances
        path = ld['LoadDistances']['Distances']
        load_distances = create_load_distances(path, load)

    return out


def create_stops(path, load):
    out = []

    for stop_inst in path:
        st = stop_inst

        stop_type = st.get('StopType', None)
        stop_location_id = st['StopLocationID']
        stop_planned_visit_date = st['StopPlannedVisitDate']

        stop_arrive_date_time = "%s %s" % (st['StopArriveDate'], st['StopArriveTime'])

        dock_date_time = None
        dock_date = st.get('DockDate', None)
        dock_time = st.get('DockTime', None)
        if dock_date and dock_time:
            dock_date_time = "%s %s" % (dock_date, dock_time)

        stop_depart_date_time = None
        stop_depart_date = st.get('StopDepartDate', None)
        stop_depart_time = st.get('StopDepartTime', None)
        if stop_depart_date and stop_depart_time:
            stop_depart_date_time = "%s %s" % (stop_depart_date, stop_depart_time)
        w60_number = st.get('W60Number', None)

        stop_location, created = Location.objects.get_or_create(code=stop_location_id)

        stop = ShiftLoadStop.objects.create(shift_load=load, stop_type=stop_type, stop_location_id=stop_location,
                                            stop_planned_visit_date=stop_planned_visit_date,
                                            stop_arrive_date_time=stop_arrive_date_time, dock_date_time=dock_date_time,
                                            stop_depart_date_time=stop_depart_date_time, w60_number=w60_number)

        ### Each stop can have many handling units
        if 'HandlingUnits' in st:
            handling_units = st['HandlingUnits']['HandlingUnit']

            if not isinstance(handling_units, list):
                handling_units = [(handling_units)]

            for hu in handling_units:
                ### Get or create handling unit name
                name = hu['HandlingUnitName']
                handling_unit, created = HandlingUnit.objects.get_or_create(handling_unit_name=name)

                handling_unit_quantity = hu['HandlingUnitQuantity']

                ShiftLoadStopHandlingUnit.objects.create(shift_load_stop=stop, handling_unit=handling_unit,
                                                         handling_unit_quantity=handling_unit_quantity)

    return out


def create_load_distances(path, load):
    out = []

    for load_dist in path:
        dist = load_dist

        distance_stop_location_id = dist['DistanceStopLocationID']
        distance_stop_arrive_date_time = "%s %s" % (dist['DistanceStopArriveDate'], dist['DistanceStopArriveTime'])
        distance_from_previous_stop = dist['DistanceFromPreviousStop']

        distance_stop_location, created = Location.objects.get_or_create(code=distance_stop_location_id)

        distance = ShiftLoadDistance.objects.create(shift_load=load,
                                                    distance_stop_location_id=distance_stop_location,
                                                    distance_stop_arrive_date_time=distance_stop_arrive_date_time,
                                                    distance_from_previous_stop=distance_from_previous_stop)
    return out


def DSImporter(xml='data/data.xml'):
    with open(xml) as fd:
        obj = json.loads(json.dumps(xmltodict.parse(fd.read()), indent=4))

        ### We first create the carrier extract object
        carrier_extract = create_carrier_extract(obj)

        ###
        driver_shifts = obj['CarrierExtract']['DriverShifts']['DriverShift']

        if not isinstance(driver_shifts, list):
            driver_shifts = [(driver_shifts)]

        for ds in driver_shifts:
            driver_shift = create_driver_shift(ds, carrier_extract)
            ###
            shifts = ds['ShiftID']

            if not isinstance(shifts, list):
                shifts = [(shifts)]

            for sh in shifts:
                shift = create_shift(sh, driver_shift)

                ###
                shift_events = create_shift_events(sh, shift)

                ###
                loads = create_loads(sh, shift)
