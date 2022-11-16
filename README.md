# Blockstars-listing-bot

This webhook posts a message on Discord everytime someone lists a new Blockstar on Magic Eden. It takes the 20 most recent listings from their API and compares the last 10 to the previous 20 most recent listings. The reason why it picks only 10 is to avoiding a delist triggering the bot because the 21th listing becomes a new listing if one of the 20 latest listings is delisted. If there's any that don't match, it calls the Blockstars API for the rating and wage attributes and posts them on the specific discord channel you attact the webhook to. 

Note: The program will fail if people list or delist more than 10 NFTs at the same time, which is unlikely but still possible
