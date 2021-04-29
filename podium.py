from PIL import Image
import requests

def generate_image(winners):
    if len(winners) <= 0:
        return False
    elif len(winners) <= 3:
        # init winners' podium
        podium = Image.open(".assets/podium.png")
        size = (80,80)
        position = [[375,40], [120,110], [605,50]] # avatar position on the image
        for index, winner in enumerate(winners):
            # create winners' podium
            winner = Image.open(requests.get(winner['avatar_url'], stream=True).raw)
            resized_avatar = winner.resize(size)
            podium.paste(resized_avatar,position[index])

        podium.save('.assets/tmp/winners.png')
        return True
    else:
        ### another winners image
        return False