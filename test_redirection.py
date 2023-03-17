# Script compares if both servers have same path redirections
import asyncio
import aiohttp
import argparse

parser = argparse.ArgumentParser(description="Script sends request to both HTTP servers with the same path and compares if it returns same URL",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-o", "--output", help="Log output file")
parser.add_argument("pathsfile", help="File containing paths, paths have to be seperated by new line and must start with /")
parser.add_argument("server1", help="sirst Server")
parser.add_argument("server2", help="second Server")
args = parser.parse_args()
config = vars(args)

SERVER1_HOST=config["server1"]
SERVER2_HOST=config["server2"]
PATHS_FILE=config["pathsfile"]
OUTPUT=config["output"]

def read_paths(file):
    paths_file = open(file, 'r')
    paths = paths_file.readlines()
    paths_file.close()
    return paths

def log(text):
    print(f'{text}\n')
    if(OUTPUT):
        log_file = open(OUTPUT, 'r')
        log_file.writelines(f'{text}\n')
        log_file.close()

async def send_request(session, url):
    async with session.get(url) as response:
        return response.url

async def compare_urls(paths):
    for path in paths:
        async with aiohttp.ClientSession() as session:
            server1_response = await send_request(session, SERVER1_HOST+path)
            server2_response = await send_request(session, SERVER2_HOST+path)
            
            if(server1_response != server2_response):
                log(server1_response)
            

def main():
    paths = read_paths(PATHS_FILE)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(compare_urls(paths))
    

if __name__ == "__main__":
    main()