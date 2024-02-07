import os
import requests
from tqdm import tqdm
import discord

def validate_file_path(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: The specified file '{file_path}' does not exist.")
        return False
    return True

def is_media_file(filename):
    media_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mp3']
    return any(filename.lower().endswith(ext) for ext in media_extensions)

def download_media(url, destination_folder=".", max_file_size_mb=24):
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  

        if total_size > max_file_size_mb * 1024 * 1024:
            print(f"Skipping {url}: File size exceeds {max_file_size_mb} MB.")
            return

        with open(destination_folder, 'wb') as file, tqdm(
            desc=os.path.basename(url),
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(block_size):
                bar.update(len(data))
                file.write(data)

        print(f"\nDownloaded: {os.path.basename(url)}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def collect_links(channel_id, headers):
    links = []

    url = f'https://discord.com/api/v10/channels/{channel_id}/messages'
    params = {'limit': 100}

    while True:
        response = requests.get(url, headers=headers, params=params)
        messages = response.json()

        for message in messages:
            if 'attachments' in message:
                for attachment in message['attachments']:
                    if 'url' in attachment:
                        links.append(attachment['url'])

            if 'embeds' in message:
                for embed in message['embeds']:
                    if 'image' in embed and 'url' in embed['image']:
                        links.append(embed['image']['url'])

                    if 'video' in embed and 'url' in embed['video']:
                        links.append(embed['video']['url'])

        if len(messages) < 100:
            break

        last_message_id = messages[-1]['id']
        params['before'] = last_message_id

    return links

def process_links(input_file, output_folder=".", max_file_size_mb=24):
    with open(input_file, 'r') as file:
        links = file.read().splitlines()

    for link in links:
        modified_link = link.split('?ex=')[0]
        download_media(modified_link, os.path.join(output_folder, os.path.basename(modified_link)), max_file_size_mb)

def run_discord_bot(token):
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'Logged in as {client.user.name}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('!pulse'):
            args = message.content.split()

            if len(args) != 3:
                await message.channel.send('Usage: !pulse <channel_id> <directory_path>')
                return

            channel_id = int(args[1])
            directory_path = args[2]

            channel = client.get_channel(channel_id)

            if not channel:
                await message.channel.send(f"Invalid channel ID: {channel_id}")
                return

            if not os.path.exists(directory_path):
                await message.channel.send(f"Invalid directory path: {directory_path}")
                return

            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)

                if os.path.isfile(file_path) and is_media_file(filename):
                    try:
                        with open(file_path, 'rb') as file:
                            await channel.send(file=discord.File(file))
                    except Exception as e:
                        print(f"Failed to upload {filename}: {e}")

            await message.channel.send("cyanide ❤️‍ FTW!")

    client.run(token)



def home_screen():
    print("\n")
    print("\033[1;36m" + " " * 20 + "PulseCord [Crafted with ❤️‍  by Cyanide]" + " " * 20 + "\033[0m")
    print("\n")
    print("Select which part to run:")
    print("\033[1;33m" + "1. Collect links from Discord channel")
    print("2. Download media from links file")
    print("3. Upload media to Discord channel")
    print("4. Exit" + "\033[0m")
    print()

def select_option():
    return input("\033[1m" + "Enter your choice (1/2/3/4): " + "\033[0m")

def main():
    while True:
        home_screen()
        option = select_option()

        if option == "1":
            user_token = input("Enter your Discord token: ")
            channel_id = input("Enter the Discord channel ID: ")
            channel_links = collect_links(channel_id, {'Authorization': user_token})
            with open(f'{channel_id}_links.txt', 'w') as f:
                for link in channel_links:
                    f.write(link + '\n')
            print('\033[92m' + 'Completed.' + '\033[0m\n')

        elif option == "2":
            input_file_path = input("Enter the path to the text file: ")
            if not validate_file_path(input_file_path):
                continue
            output_folder_path = input("Enter the path to the output folder: ")
            os.makedirs(output_folder_path, exist_ok=True)
            max_file_size_mb = int(input("Enter the maximum file size to download (in MB): "))
            process_links(input_file_path, output_folder_path, max_file_size_mb)
            print('\033[92m' + 'Completed.' + '\033[0m\n')

        elif option == "3":
            user_token = input("Enter your Discord token: ")
            run_discord_bot(user_token)

        elif option == "4":
            print("\033[93m" + "Exiting..." + "\033[0m")
            break

        else:
            print("\033[91m" + "Invalid option selected. Please choose a valid option (1/2/3/4)." + "\033[0m")

if __name__ == "__main__":
    main()
