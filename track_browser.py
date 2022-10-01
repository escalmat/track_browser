import sys
sys.path.append('C:\\Users\\User\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python39\\site-packages')
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp_c
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, InvalidArgumentException, WebDriverException, NoSuchWindowException
from time import sleep

import tempfile



def track_name_by_url(url, driver):

    track_name_xpaths = ['/html/body/div[3]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[1]/div[5]/span/h1',
                        '/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[1]/div[5]/span/h1']
    track_name = None

    try:

        driver.get( url )
        wait = WebDriverWait(driver, 20)

    except WebDriverException:
        print("error with webdriver")
        pass

    else:

        for xpath in track_name_xpaths:

            try:
                track_name_elm = WebDriverWait( driver, 10 ).until( exp_c.presence_of_element_located( (By.XPATH, xpath) ) )
            except TimeoutException:
                pass
            else:
                if track_name_elm.text != '' and track_name_elm.text != ' ' and track_name_elm.text is not None:
                    track_name = track_name_elm.text
                    print("track name found: {}".format(track_name) )
                    break
                else:
                    print("no track name found")
                

    return track_name



            
def get_clickeable_divs(xpath, extra_xpath, secs_wait, driver):

    try:
        WebDriverWait( driver, secs_wait + 10 ).until( exp_c.presence_of_element_located( (By.XPATH, extra_xpath) ) )
    except TimeoutException:
        print("no clickeable extra_xpath found")
        return None
    else:
        try:
            clickeable_divs = WebDriverWait( driver, secs_wait ).until( exp_c.presence_of_all_elements_located( (By.XPATH, xpath) ) )
        except TimeoutException:
            print("no clickeable divs found")
            return None
        else:
            return clickeable_divs

        


def click(elm_type, clickeable_elm_index, clickeable_divs_xpath, extra_xpath, click_call, max_click_calls, driver):

    clickeable_elms = get_clickeable_divs(xpath=clickeable_divs_xpath, extra_xpath=extra_xpath, secs_wait=5, driver=driver)
    status = 1 # click ok
    clickable_elm = None

    if clickeable_elms is None:
        return 2

    if clickeable_elm_index == len( clickeable_elms ):
        return 2

    if elm_type == 1:

        try:
            clickable_elm = clickeable_elms[ clickeable_elm_index ].find_element( By.XPATH, './div[1]' ) # first div of clickable_elm fires the event
        except NoSuchElementException:
            return 2

    elif elm_type == 2:

        try:
            clickable_elm = clickeable_elms[ clickeable_elm_index ].find_element( By.XPATH, './label/input' ) # first div of clickable_elm fires the event
        except NoSuchElementException:
            return 2
        

    print("trying to click element with text: {}".format( clickeable_elms[ clickeable_elm_index ].text ) )
    

    try:
                
        driver.execute_script( "arguments[0].click();", clickable_elm )   # it triggers a javascript event
                
    except StaleElementReferenceException:
        if click_call[0] <= max_click_calls:
            click_call[0] += 1
            status = click(clickeable_elm_index,
                               clickeable_divs_xpath,
                               click_call,
                               max_click_calls,
                               driver)
        else:
            status = 0
    except ElementClickInterceptedException:
        if click_call[0] <= max_click_calls:
            click_call[0] += 1
            status = click(clickeable_elm_index,
                               clickeable_divs_xpath,
                               click_call,
                               max_click_calls,
                               driver)
        else:
            status = 0
    except ElementNotInteractableException:
        print("element not interactable")
        return 2
    except NoSuchElementException:
        if click_call[0] <= max_click_calls:
            click_call[0] += 1
            status = click(clickeable_elm_index,
                               clickeable_divs_xpath,
                               click_call,
                               max_click_calls,
                               driver)
        else:
            status = 0
    else:
        print(">>> [{}] click OK".format( clickeable_elms[ clickeable_elm_index ].text ) )
            

    return status # set with the value of the last click function call




def check_for_track_name( track_name ):
    
    tracks_xpath = '/html/body/div[4]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div/section/div[2]/div[3]/div/div[2]/div[2]/div'
    track_name_xpath = './div/div[2]/div/a/div'

    try:
        tracks_divs = WebDriverWait( driver, 20 ).until( exp_c.presence_of_all_elements_located( (By.XPATH, tracks_xpath) ) )
    except TimeoutException:
        pass
    else:

        track_name_found = None

        for i in range( len( tracks_divs ) ):

            try:
                track_name_found = tracks_divs.find_element( By.XPATH, track_name_xpath ).text
            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                pass
            except WebDriverException:
                pass
            else:

                if track_name == track_name_found:
                    # write playlist url into a txt file
                    print("track [%s] found in playlist at: %s", track_name, link )
                    break


def check_in_playlists(three_d_matrix, track_name, driver):

    

    for two_d_matrix in three_d_matrix:

        for list_ in two_d_matrix:

            for elm in list_:

                prev_click_url = driver.current_url

                try:
                    driver.get( elm )
                    WebDriverWait( driver, 20 ).until( lambda driver: driver.current_url != prev_click_url )
                except TimeOutException:
                    print( "playlist don't load, 2nd attempt" )
                    pass
                except WebDriverExeption:
                    print( "playlist don't load, 2nd attempt" )
                    pass
                else:

                    # -------------------- now i'm IN SPOTIFY --------------------------
                    
                    check_for_track_name( track_name )
        

                

        



def display_name_list( elms, init_index, current_index ):

    for i in range(init_index, len(elms)):

        if elms[ i ].text == '' or elms[ i ].text == ' ':
            print( "    empty")
        elif i == current_index:
            print( ">>> {}".format( elms[ i ].text ) )
        else:
            print( "    {}".format( elms[ i ].text ) )


# go through every playlist to check for the track name

def browse_through_playlists(desired_track_name, driver):

    genres_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div/div'
    sub_gen_xpath = '/html/body/div[1]/div/div[3]/div/div[2]/div/div[3]/div[2]/div/div' # it appears after a javascript event
    link_xpath = './div[1]/div[1]/div[2]/div/div[1]/div/a'
    playlists_xpath = '/html/body/div[1]/div/div[3]/div/div[3]/div[4]/div'              # it appears after a javascript event
    playlists_divs = None

    genres_divs = None
    sub_gen_divs = None
    track_name_found = ''
    clickeable_gen_index = 2
    clickeable_subgen_index = 0

    playlists_links_list = [][][] # [n][k][i]; n = genre, k = subgenre, i = playlist

 
    genre_divs = get_clickeable_divs(xpath=genres_xpath,
                                     extra_xpath='/html/body/div[1]/div/div[3]/div/div[2]/div/div[3]',
                                     secs_wait=20,
                                     driver=driver)
    

    
     
    if len(genre_divs) <= 2:
        print("error while clicking")
        return
    
    
    for n in range(2, len(genre_divs)):

        if genre_divs[ n ].text == '' or genre_divs[ n ].text == ' ':
            continue

        display_name_list( genre_divs, 2, n )

        # ------------------ GENRE ------------------------

        status_gen = click( elm_type=1,
                            clickeable_elm_index=n,
                            clickeable_divs_xpath=genres_xpath,
                            extra_xpath='/html/body/div[1]/div/div[3]/div/div[2]/div/div[3]',
                            click_call=[0],
                            max_click_calls=5,
                            driver=driver )

        if status_gen == 2:
            print("no genres")
            break
        

        if status_gen == 1:

            print("\n>>> trying to id sub-elements of {}\n".format( genre_divs[ n ].text ))

            genre_divs = get_clickeable_divs(xpath=sub_gen_xpath,
                                             extra_xpath='/html/body/div[1]/div/div[3]/div/div[2]/div/div[3]',
                                             secs_wait=20,
                                             driver=driver)


            if len(genre_divs) == 0:
                print("no subgenres divs")
                return

    
            for k in range( len(genre_divs) ):

                if genre_divs[ k ].text == '' or genre_divs[ k ].text == ' ':
                    continue

                display_name_list( genre_divs, 0, k )

                # --------------------------- SEBGENRE -------------------------------
            
                status_subgen = click( elm_type=2,
                                       clickeable_elm_index=k,
                                       clickeable_divs_xpath=sub_gen_xpath,
                                       extra_xpath='/html/body/div[1]/div/div[3]/div/div[2]/div/div[3]',
                                       click_call=[0],
                                       max_click_calls=5,
                                       driver=driver )

                if status_subgen == 2:
                    print("no subgenres")
                    break

                if status_subgen == 1:

                    try:
                        
                        # capture the NEW CONTENT in the doc ----> PLAYLISTS          
                        playlists_divs = WebDriverWait( driver, 20 ).until( exp_c.presence_of_all_elements_located( (By.XPATH, playlists_xpath) ) )
                        
                    except TimeoutException:
                        print("no playlist found")
                        pass
                    else:

                        link = None

                        for i in range( len( playlists_divs ) ):

                            try:
                                link = playlists_divs[ i ].find_element( By.XPATH, link_xpath ).get_attribute( 'href' )
                            except NoSuchElementException:
                                pass
                            except WebdriverException:
                                pass
                            else:
                                playlists_links_list[n][k].append( link )


                            
                        status_subgen = click( elm_type=2,
                                               clickeable_elm_index=k,
                                               clickeable_divs_xpath=sub_gen_xpath,
                                               extra_xpath='/html/body/div[1]/div/div[3]/div/div[2]/div/div[3]',
                                               click_call=[0],
                                               max_click_calls=5,
                                               driver=driver )

                        if status_subgen != 1:
                            print("can't click subgenres again")
                            


            status_gen = click( elm_type=1,
                                clickeable_elm_index=n,
                                clickeable_divs_xpath=genres_xpath,
                                extra_xpath='/html/body/div[1]/div/div[3]/div/div[2]/div/div[3]',
                                click_call=[0],
                                max_click_calls=5,
                                driver=driver )

            if status_gen != 1:
                print("can't click genres again")
                
                            

    check_in_playlists( playlists_links_list,
                        desired_track_name,
                        driver )

                    
        

def go_to_playlists_doc(url, desired_track_name, driver):

    #check_in_playlist
    #browse_through_playlists

    desired_url = 'https://dailyplaylists.com/submit-song-1'
    track_s_box_xpaths = ['/html/body/div[1]/div/div[3]/div[2]/div[1]/input',
                         '/html/body/div[1]/div/div[4]/div[2]/div[1]/input']
    ok_button_xpath = '/html/body/div[1]/div/div[3]/div/div/div[3]/div[2]/div[2]/button'
    track_s_box_elm = None

    try:

        driver.get( url )
        wait = WebDriverWait(driver, 20)

    except WebDriverException:
        print("webdriver error at: {}".format(url) )
        pass

    else:

        for xpath in track_s_box_xpaths:
            
            try:
                track_s_box_elm = WebDriverWait( driver, 20 ).until( exp_c.presence_of_element_located( (By.XPATH, xpath) ) )
            except TimeoutException:
                track_s_box_elm = None
                print("first attempt failed")
            except WebDriverException:
                track_s_box_elm = None
                print("webdriver error while trying to locate search box")
                pass
            else:
                break
                
                
        if track_s_box_elm is not None:

            
            track_s_box_elm.send_keys('') # random song
            

            # if "that's right continue botton"
            try:
                btn_elm = WebDriverWait( driver, 20 ).until( exp_c.presence_of_element_located( ( By.XPATH, ok_button_xpath ) ) )
            except TimeoutException:
                print("ok button doesn't found")
                pass
            else:

                try:
                    driver.execute_script( "arguments[0].click();", btn_elm )
                except ElementClickInterceptedException:
                    print("bad continue button")
                    return
                except ElementNotInteractableException:
                    print("bad continue button")
                    return
                except NoSuchElementException:
                    print("bad continue button")
                    return
                    
                desired_url = 'https://dailyplaylists.com/submit-song-2'
                    
                try:
                    WebDriverWait( driver, 20 ).until(lambda driver: driver.current_url == desired_url)
                except TimeoutException:
                    print("desired page 2 doesn't load")
                    pass
                else:
                    browse_through_playlists(desired_track_name=desired_track_name,
                                             driver=driver)



if __name__ == "__main__":


    opts = Options()
    opts.add_argument("-profile")
    opts.add_argument("") # your profile

    service = webdriver.firefox.service.Service('geckodriver', service_args=["--marionette-port", "2828"])
    driver = webdriver.Firefox(options=opts, service=service)
    driver.implicitly_wait(1)

 

    spotify_track_name = track_name_by_url(url=sys.argv[1],
                                           driver=driver)

    

    service = webdriver.firefox.service.Service('geckodriver', port=9024)
    driver = webdriver.Firefox(service=service)
    driver.implicitly_wait(1)

  

    if spotify_track_name is not None:
    
        go_to_playlists_doc(url='https://dailyplaylists.com/',
                            desired_track_name=spotify_track_name,
                            driver=driver)
    
    try:
        driver.stop_client()
        driver.close()
        driver.quit()
    except NoSuchWindowException:
        print("coundn't close driver propertly")
        pass

