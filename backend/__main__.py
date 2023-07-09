print('test')

from hub.Hub import Hub


# put all backend initialization stuff here
def main():
    # create hub- the hub should create everything it's immediately attached to upon startup
    hub = Hub()

    # start hub
    hub.start()


main()
