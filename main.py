# Blockstars Listing Bot
from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import os
import json
import time
import re
from replit_keep_alive import keep_alive


collection =  'blockstars'
# Collecting the webhook URLs
webhook_url1 = os.environ['webhook_url1']
webhook_urls = webhook_url1


def new_listing_discord(webhook_urls, price, url_token, current_star_rating, potential_star_rating, bucket, percent_cut, salary, serial_number, image):
  """ Writes a message about the new listing on discord"""

  webhook = DiscordWebhook(url=webhook_urls)

  # Create embed object for webhook
  embed = DiscordEmbed(title='New listing!', description='Blockstar #'+str(serial_number), color='03b2f8')

  # Set author (in this case the link to the listing on ME)
  embed.set_author(name='Link to Magic Eden', url=url_token,                  icon_url='https://pbs.twimg.com/profile_images/1554554723423993857/owxazkRR_400x400.jpg')

  # set image
  embed.set_image(url=image)

  # Set footer
  embed.set_footer(text='powered by KioNFTguy', icon_url='https://assets.blockstars.gg/images/16_portrait.png')

  # Set timestamp (default is now)
  embed.set_timestamp()

  # Add fields to embed
  embed.add_embed_field(name='Price', value=str(price) + ' SOL')
  embed.add_embed_field(name='Star rating', value=str(current_star_rating)+"/"+str(potential_star_rating))
  embed.add_embed_field(name='Wage', value=str(salary) + ' | ' + str(bucket) + ' (' + str(int(percent_cut*100)) + '% cut)')

  # Add embed object to webhook
  webhook.add_embed(embed)

  response = webhook.execute()
  

# Calling the ME API and getting the 20 most recent listings
url_ME = requests.get("https://api-mainnet.magiceden.dev/v2/collections/"+collection+"/listings?offset=0&limit=20") 

# Turn data into a json file
data_old = json.loads(url_ME.text)

while True:

  # Call the ME API again and get the new 20 most recent listings
  url_ME = requests.get("https://api-mainnet.magiceden.dev/v2/collections/"+collection+"/listings?offset=0&limit=20") 

  # Turn data into a json file
  data_new = json.loads(url_ME.text)

  # Get the list of token addresses
  token_mint_list_old = []
  token_mint_list_new = []
  for token in data_old:
    token_mint_list_old.append(token["tokenMint"])
  for token in data_new:
    token_mint_list_new.append(token["tokenMint"])

  # Check if the listing is new and if it is on the 10 most recent       ones (to avoid delistings creating a false new listing)
  # Note: The program will fail if people list or delist more than 10 NFTs at the same time, which is unlikely but still possible
  for token in data_new:
    if not token['tokenMint'] in token_mint_list_old:
      if token['tokenMint'] in token_mint_list_new[:10]:
        
        # Extract the serial number using the img url provided
        serial_number = re.sub(r'\D+', '', token['extra']['img'])
        # Call blockstars API
        url_blockstars =  requests.get('https://app.blockstars.gg/api/blockstar/'+serial_number)
        # Turn the data into a json file
        data_blockstars = json.loads(url_blockstars.text)
        # Collect the information we need
        current_star_rating = data_blockstars['starRatingInfo']['currentStarRating']
        potential_star_rating = data_blockstars['starRatingInfo']['maxStarRating']
        bucket = data_blockstars['wage']['bucket']
        percent_cut = data_blockstars['wage']['percentCut']
        salary = data_blockstars['wage']['salary']
        image = token['extra']['img']
        price = token['price']
        url_token = "https://magiceden.io/item-details/"+token['tokenMint']
        

        new_listing_discord(webhook_urls, price, url_token, current_star_rating, potential_star_rating, bucket, percent_cut, salary, serial_number, image)


  data_old = data_new
  time.sleep(120)
  keep_alive()
