*** Settings ***
Library    Seatbelt_methods.py

*** Keywords ***
Initialize Seatbelt System
    Fasten Seatbelt
    Stop Engine
    Person Leaves
    Set Vehicle Speed    0

*** Test Cases ***

#CR_1
Test Seatbelt Alerts
    [Documentation]    Check that light and sound alerts function correctly when the seatbelt is unfastened and fastened.
    [Setup]    Initialize Seatbelt System

    Unfasten Seatbelt
    ${light_yellow}=    Is Light Indicator Yellow
    ${sound_on}=    Is Sound Alarm On
    ${sound_off}=  Set Variable    ${sound_on} == False
    Should Be True    ${light_yellow}    The warning light should be yellow when the belt is unfastened.
    Should Be True    ${sound_off}    The audible alarm should be deactivated when the belt is unfastened.

    Start Engine
    Person Sits
    Set Vehicle Speed    70
    ${light_red}=    Is Light Indicator Red
    ${sound_on}=    Is Sound Alarm On
    Should Be True    ${light_red}    The warning light should be red when the seatbelt is not fastened, the engine is running, a person is present, and the speed is over 40 km/h.
    Should Be True    ${sound_on}    The audible alarm must be activated when the seatbelt is not fastened, the engine is switched on, a person is present, and speed exceeds 40 km/h.

    Fasten Seatbelt
    ${light_green}=    Is Light Indicator Green
    ${sound_on}=    Is Sound Alarm On
    ${sound_off}=  Set Variable    ${sound_on} == False
    Should Be True    ${light_green}    The warning light should be green when the belt is fastened.
    Should Be True    ${sound_off}    The audible alarm must be deactivated when the belt is fastened.

#CR_2
Test Engine Off
    [Documentation]    Check that the audible alarm does not sound when the engine is switched off and the indicator light is yellow.
    Start Engine
    Unfasten Seatbelt
    Stop Engine
    ${light_yellow}=    Is Light Indicator Yellow
    ${sound_on}=    Is Sound Alarm On
    ${sound_off}=  Set Variable    ${sound_on} == False
    Should Be True    ${light_yellow}    The warning light should be yellow when the engine is off.
    Should Be True    ${sound_off}    The audible alarm must not be activated when the engine is switched off.

#CR_3
Test Person Not Present
    [Documentation]    Check that the audible alarm does not go off when no-one is in the seat and the indicator light is yellow.
    Start Engine
    Unfasten Seatbelt
    Person Leaves
    ${light_yellow}=    Is Light Indicator Yellow
    ${sound_on}=    Is Sound Alarm On
    ${sound_off}=  Set Variable    ${sound_on} == False
    Should Be True    ${light_yellow}    The warning light should be yellow when no one is in the seat.
    Should Be True    ${sound_off}    The audible alarm must not be activated when no one is sitting on the seat.

#CR_4
Test Speed Less Than 40
    [Documentation]    Check that the audible alarm does not sound when vehicle speed is below 40 km/h and the indicator light is yellow.
    Start Engine
    Person Sits
    Unfasten Seatbelt
    Set Vehicle Speed    20
    ${light_yellow}=    Is Light Indicator Yellow
    ${sound_on}=    Is Sound Alarm On
    ${sound_off}=  Set Variable    ${sound_on} == False
    Should Be True    ${light_yellow}    The warning light should be yellow when speed is below 40 km/h.
    Should Be True    ${sound_off}    The audible alarm should not be activated at speeds below 40 km/h.

#CR_5
Test All Conditions Met
    [Documentation]    Check that the audible alarm sounds when the seatbelt is not fastened, the engine is running, a person is present and the speed is greater than or equal to 40 km/h.
    Start Engine
    Person Sits
    Unfasten Seatbelt
    Set Vehicle Speed    65
    ${light_red}=    Is Light Indicator Red
    ${sound_on}=    Is Sound Alarm On
    Should Be True    ${light_red}    The warning light should be red when all conditions are met.
    Should Be True    ${sound_on}    The audible alarm must be activated when all conditions are met.
