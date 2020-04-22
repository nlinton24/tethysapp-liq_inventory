from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import (Button, MapView, TextInput, DatePicker,
                               SelectInput, DataTableView, MVDraw, MVView,
                               MVLayer)
from tethys_sdk.workspaces import app_workspace
from .model import add_new_site, get_all_sites


@login_required()
def home(request):
    """
    Controller for the app home page.
    """


    save_button = Button(
        display_text='',
        name='save-button',
        icon='glyphicon glyphicon-floppy-disk',
        style='success',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='glyphicon glyphicon-edit',
        style='warning',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='glyphicon glyphicon-remove',
        style='danger',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Next'
        }
    )

    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button
    }

    return render(request, 'liq_inventory/home.html', context)

@login_required()
def about(request):
    """
    Controller for the background page.
    """
    context = {}

    return render(request,'liq_inventory/about.html',context)

@login_required()
def help(request):
    """
    Controller for the background page.
    """
    context = {}

    return render(request,'liq_inventory/help.html',context)

@app_workspace
@login_required()
def addloc(request, app_workspace):
    """
    Controller for the Add Dam page.
    """
    # Default Values
    country = ''
    city = ''
    lat = ''
    date_eq = ''
    long = ''

    # Errors
    country_error = ''
    city_error = ''
    lat_error = ''
    date_error = ''
    long_error = ''

    # Handle form submission
    if request.POST and 'add-button' in request.POST:
        # Get values
        has_errors = False
        country = request.POST.get('country', None)
        city = request.POST.get('city', None)
        lat = request.POST.get('lat', None)
        date_eq = request.POST.get('date-eq', None)
        long = request.POST.get('long', None)

        # Validate
        if not country:
            has_errors = True
            country_error = 'Country is required.'

        if not city:
            has_errors = True
            city_error = 'City is required.'

        if not lat:
            has_errors = True
            lat_error = 'Lattitude is required.'

        if not date_eq:
            has_errors = True
            date_error = 'Date of earthquake is required.'

        if not long:
            has_errors = True
            long_error = 'Longitude is required.'

        if not has_errors:
            add_new_site(db_directory=app_workspace.path, long=long, country=country, city=city, lat=lat, date_eq=date_eq)
            return redirect(reverse('liq_inventory:home'))

        messages.error(request, "Please fix errors.")

    # Define form gizmos
    country_input = TextInput(
        display_text='Country',
        name='country',
        initial=country,
        error=country_error
    )

    city_input = TextInput(
        display_text='City',
        name='city',
        initial=city,
        error=city_error
    )

    lat_input = TextInput(
        display_text='Lattitude',
        name='lat',
        initial=lat,
        error=lat_error
    )

    long_input = TextInput(
        display_text='Longitude',
        name='long',
        initial=long,
        error=long_error
    )

    date_eq = DatePicker(
        name='date-eq',
        display_text='Date of Earthquake',
        autoclose=True,
        format='MM d, yyyy',
        start_view='decade',
        today_button=True,
        initial=date_eq,
        error=date_error
    )

    initial_view = MVView(
        projection='EPSG:4326',
        center=[-98.6, 39.8],
        zoom=3.5
    )

    drawing_options = MVDraw(
        controls=['Modify', 'Delete', 'Move', 'Point'],
        initial='Point',
        output_format='GeoJSON',
        point_color='#FF0000'
    )

    add_button = Button(
        display_text='Add',
        name='add-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'add-site-form'},
        submit=True
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('liq_inventory:home')
    )

    context = {
        'country_input': country_input,
        'city_input': city_input,
        'lat_input': lat_input,
        'date_eq_input': date_eq,
        'long_input': long_input,
        'add_button': add_button,
        'cancel_button': cancel_button,
    }

    return render(request, 'liq_inventory/addloc.html', context)

@app_workspace
@login_required()
def list_sites(request, app_workspace):
    """
    Show all dams in a table view.
    """
    sites = get_all_sites(app_workspace.path)
    table_rows = []

    for site in sites:
        table_rows.append(
            (
                site['country'], site['city'],
                site['lat'], site['long'], site['date_eq']
            )
        )

    sites_table = DataTableView(
        column_names=('Country', 'City', 'Lattitude', 'Longitude', 'Date of Earthquake'),
        rows=table_rows,
        searching=False,
        orderClasses=False,
        lengthMenu=[ [10, 25, 50, -1], [10, 25, 50, "All"] ],
    )

    context = {
        'sites_table': sites_table
    }

    return render(request, 'liq_inventory/list_sites.html', context)
