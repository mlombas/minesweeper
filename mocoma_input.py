"""Provides some helper methods and classes to work with input in pygame"""

import pygame

def prompt(surface, message, rect=pygame.Rect(0, 0, 100, 100), bg_color=(0, 0, 0), text_color=(255, 255, 255)):
    """Will prompt the user with a message and return what the user inputs.
    
    Please note that this method is async, it will stop execution until the
    user inputs something.

    Input:
        surface - the surface to show the prompt box
        message - the message to prompt
        x - the x coordinate of the top left corner
        y - the y coordinate of the top left corner
        width - the width of the box
        height - the height of the box

    Output:
        The string inputed by the user as the answer
    """

    box = pygame.Surface((rect.width, rect.height))
    introduced = ""
    if not pygame.font.get_init(): pygame.font.init()
    font = pygame.font.SysFont(None, int(rect.height * 0.9 / 2)) #Leave 10% for margin
    while True: #Wait until next event, if its a keyboard event process it
        #Draw all box
        box.fill(bg_color) #TODO make the text become smaller if needed
        message_width, message_height = font.size(message) #TODO fix this garbage and make it more readable
        box.blit(font.render(message, 0, text_color), ((rect.width - message_width)/2, (rect.height/2 - message_height)/2)) #Print message, adjust to be on middle
        introduced_width, introduced_height = font.size(introduced)
        box.blit(font.render(introduced, 0, text_color), ((rect.width - introduced_width)/2, rect.height/2 + (rect.height/2 - introduced_height)/2)) #Print the input so far, adjust it also
        surface.blit(box, rect)
        pygame.display.update()

        #Wait for input
        evt = pygame.event.wait()
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_BACKSPACE:
                introduced = introduced[:-1]
            elif evt.key == pygame.K_RETURN:
                return introduced #If the user presses enter, return the inputs
            else:
                introduced += evt.unicode            
   
