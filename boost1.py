import requests
import uuid
import time
import random
import sys
from urllib.parse import urlparse
import os

# Modern Color Scheme
class Colors:
    PRIMARY = '\x1b[38;5;147m'      # Soft Purple
    SECONDARY = '\x1b[38;5;117m'    # Soft Blue
    SUCCESS = '\x1b[38;5;156m'      # Mint Green
    WARNING = '\x1b[38;5;222m'      # Soft Yellow
    ERROR = '\x1b[38;5;210m'        # Soft Red
    ACCENT = '\x1b[38;5;183m'       # Lavender
    TEXT = '\x1b[38;5;255m'         # White
    DIM = '\x1b[38;5;245m'          # Gray
    RESET = '\x1b[0m'
    BOLD = '\x1b[1m'

ASCII_ART = f"""{Colors.PRIMARY}
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║          {Colors.BOLD}®  TikTok Booster  ®{Colors.RESET}{Colors.PRIMARY}                   ║
    ║                                                      ║
    ║              {Colors.SECONDARY} by Donut {Colors.RESET}{Colors.PRIMARY}                          ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
{Colors.RESET}"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print(ASCII_ART)
    print(f"\n{Colors.DIM}{'─' * 60}{Colors.RESET}")
    print(f"{Colors.TEXT}    V2  |  Professional Engagement Tool{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}\n")

def print_progress_bar(iteration, total, prefix='', suffix='', length=40):
    percent = '{0:.1f}'.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    
    # Gradient effect
    bar = '█' * filled_length + '░' * (length - filled_length)
    
    sys.stdout.write(f'\r{Colors.TEXT}{prefix} {Colors.SECONDARY}[{bar}] {Colors.PRIMARY}{percent}%{Colors.RESET} {Colors.DIM}{suffix}{Colors.RESET}')
    sys.stdout.flush()

class TikTokUnlimitedBooster:
    def __init__(self):
        self.base_url = 'https://zefame-free.com/api_free.php'
        self.proxy_url = 'https://zefame-free.com/tiktok_proxy.php'
        self.device_id = str(uuid.uuid4())
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        ]
        self.device_ids = [str(uuid.uuid4()) for _ in range(10)]
        self.current_device_index = 0

    def get_headers(self):
        return {
            'user-agent': random.choice(self.user_agents),
            'accept': 'application/json',
            'origin': 'https://zefame.com',
            'referer': 'https://zefame.com/',
            'x-request-id': str(uuid.uuid4()),
            'x-timestamp': str(int(time.time() * 1000))
        }

    def get_next_device_id(self):
        device_id = self.device_ids[self.current_device_index]
        self.current_device_index = (self.current_device_index + 1) % len(self.device_ids)
        return device_id

    def extract_video_id(self, tiktok_url):
        parsed = urlparse(tiktok_url)
        path_parts = parsed.path.split('/')
        for i, part in enumerate(path_parts):
            if part == 'video' and i + 1 < len(path_parts):
                return path_parts[i + 1].split('?')[0]
        return None

    def bypass_check_video_id(self, tiktok_url):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                headers = self.get_headers()
                headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
                
                data = {
                    'action': 'checkVideoId',
                    'link': tiktok_url
                }
                
                response = self.session.post(self.base_url, headers=headers, data=data, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success') or result.get('status') == 'success':
                        video_id = result.get('data', {}).get('videoId') or result.get('videoId')
                        if video_id:
                            return video_id
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f'{Colors.WARNING}[Retry {attempt + 1}] {e}{Colors.RESET}')
                time.sleep(random.uniform(2, 4))
        
        return None

    def bypass_check_service(self, video_id, service_id):
        for _ in range(2):
            try:
                device_id = self.get_next_device_id()
                params = {
                    'action': 'check',
                    'device': device_id,
                    'service': service_id,
                    'videoId': video_id,
                    '_': str(int(time.time() * 1000))
                }
                
                headers = self.get_headers()
                response = self.session.get(self.base_url, headers=headers, params=params, timeout=8)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success') or result.get('status') == 'success':
                        allowed = result.get('data', {}).get('allowed') or result.get('available')
                        if allowed:
                            return True
                
                time.sleep(random.uniform(1, 2))
            except:
                pass
        
        return False

    def bypass_place_order(self, tiktok_url, video_id, service_id):
        order_attempts = 2
        
        for attempt in range(order_attempts):
            try:
                device_id = self.get_next_device_id()
                headers = self.get_headers()
                headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
                
                data = {
                    'action': 'order',
                    'service': service_id,
                    'link': tiktok_url,
                    'uuid': device_id,
                    'videoId': video_id,
                    'timestamp': str(int(time.time() * 1000))
                }
                
                url = f"{self.base_url}?action=order&_={int(time.time() * 1000)}"
                response = self.session.post(url, headers=headers, data=data, timeout=10)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if result.get('success'):
                        order_id = result.get('data', {}).get('orderId', 'N/A')
                        return {
                            'success': True,
                            'order_id': order_id,
                            'message': 'Order placed successfully!'
                        }
                    
                    msg = str(result.get('message', '')).lower()
                    if 'limit' in msg:
                        wait_time = random.uniform(30, 60)
                        print(f"{Colors.WARNING}  ⏱  Rate limit - waiting {wait_time:.1f}s{Colors.RESET}")
                        time.sleep(wait_time)
                
            except Exception as e:
                print(f"{Colors.ERROR}  ✗  Attempt {attempt + 1}: {e}{Colors.RESET}")
            
            time.sleep(random.uniform(5, 10))
        
        return {'success': False, 'message': 'Failed after multiple attempts'}

    def unlimited_boost_views(self, tiktok_url, boost_count=100):
        print(f'\n{Colors.PRIMARY}{"═" * 60}')
        print(f'{Colors.BOLD}  👁  Views Boost Campaign{Colors.RESET}')
        print(f'{Colors.PRIMARY}{"═" * 60}{Colors.RESET}\n')
        
        video_id = self.bypass_check_video_id(tiktok_url)
        if not video_id:
            print(f'{Colors.ERROR}  ✗  Could not extract video ID{Colors.RESET}')
            return False
        
        print(f'{Colors.SUCCESS}  ✓  Video ID: {Colors.TEXT}{video_id}{Colors.RESET}')
        print(f'{Colors.DIM}  Target: {boost_count} views\n{Colors.RESET}')
        
        successful_boosts = 0
        failed_boosts = 0
        
        for boost_num in range(1, boost_count + 1):
            print(f'\n{Colors.TEXT}  Boost #{boost_num}{Colors.RESET}')
            
            for i in range(20):
                print_progress_bar(i, 20, prefix='  ', suffix='Checking')
                time.sleep(0.03)
            
            if self.bypass_check_service(video_id, 229):
                for i in range(20):
                    print_progress_bar(i, 20, prefix='  ', suffix='Processing')
                    time.sleep(0.03)
                
                result = self.bypass_place_order(tiktok_url, video_id, 229)
                
                if result['success']:
                    successful_boosts += 1
                    print(f'\n{Colors.SUCCESS}  ✓  Success! Order: {result["order_id"]}{Colors.RESET}')
                else:
                    failed_boosts += 1
                    print(f'\n{Colors.WARNING}  ⚠  Skipped: {result["message"]}{Colors.RESET}')
            else:
                failed_boosts += 1
                print(f'\n{Colors.WARNING}  ⚠  Service unavailable{Colors.RESET}')
            
            # Stats
            total = successful_boosts + failed_boosts
            rate = (successful_boosts / total * 100) if total > 0 else 0
            print(f'{Colors.DIM}  Progress: {boost_num}/{boost_count} | Success: {successful_boosts} | Rate: {rate:.1f}%{Colors.RESET}')
            
            if boost_num < boost_count:
                delay = random.uniform(5, 15)
                print(f'{Colors.DIM}  Next in {delay:.1f}s...{Colors.RESET}')
                time.sleep(delay)
        
        print(f'\n{Colors.PRIMARY}{"═" * 60}')
        print(f'{Colors.SUCCESS}  ✓  Campaign Complete!{Colors.RESET}')
        print(f'{Colors.TEXT}  Total Success: {successful_boosts} | Failed: {failed_boosts}{Colors.RESET}')
        print(f'{Colors.PRIMARY}{"═" * 60}{Colors.RESET}\n')
        
        return True

    def unlimited_boost_likes(self, tiktok_url, boost_count=100):
        print(f'\n{Colors.PRIMARY}{"═" * 60}')
        print(f'{Colors.BOLD}  ❤  Likes Boost Campaign{Colors.RESET}')
        print(f'{Colors.PRIMARY}{"═" * 60}{Colors.RESET}\n')
        
        video_id = self.bypass_check_video_id(tiktok_url)
        if not video_id:
            print(f'{Colors.ERROR}  ✗  Could not extract video ID{Colors.RESET}')
            return False
        
        print(f'{Colors.SUCCESS}  ✓  Video ID: {Colors.TEXT}{video_id}{Colors.RESET}')
        print(f'{Colors.DIM}  Target: {boost_count} likes\n{Colors.RESET}')
        
        successful_boosts = 0
        failed_boosts = 0
        
        for boost_num in range(1, boost_count + 1):
            print(f'\n{Colors.TEXT}  Boost #{boost_num}{Colors.RESET}')
            
            for i in range(20):
                print_progress_bar(i, 20, prefix='  ', suffix='Checking')
                time.sleep(0.03)
            
            if self.bypass_check_service(video_id, 232):
                for i in range(20):
                    print_progress_bar(i, 20, prefix='  ', suffix='Processing')
                    time.sleep(0.03)
                
                result = self.bypass_place_order(tiktok_url, video_id, 232)
                
                if result['success']:
                    successful_boosts += 1
                    print(f'\n{Colors.SUCCESS}  ✓  Success! Order: {result["order_id"]}{Colors.RESET}')
                else:
                    failed_boosts += 1
                    print(f'\n{Colors.WARNING}  ⚠  Skipped: {result["message"]}{Colors.RESET}')
            else:
                failed_boosts += 1
                print(f'\n{Colors.WARNING}  ⚠  Service unavailable{Colors.RESET}')
            
            total = successful_boosts + failed_boosts
            rate = (successful_boosts / total * 100) if total > 0 else 0
            print(f'{Colors.DIM}  Progress: {boost_num}/{boost_count} | Success: {successful_boosts} | Rate: {rate:.1f}%{Colors.RESET}')
            
            if boost_num < boost_count:
                delay = random.uniform(5, 15)
                print(f'{Colors.DIM}  Next in {delay:.1f}s...{Colors.RESET}')
                time.sleep(delay)
        
        print(f'\n{Colors.PRIMARY}{"═" * 60}')
        print(f'{Colors.SUCCESS}  ✓  Campaign Complete!{Colors.RESET}')
        print(f'{Colors.TEXT}  Total Success: {successful_boosts} | Failed: {failed_boosts}{Colors.RESET}')
        print(f'{Colors.PRIMARY}{"═" * 60}{Colors.RESET}\n')
        
        return True

    def dual_boost_views_likes(self, tiktok_url, boost_count=100):
        print(f'\n{Colors.PRIMARY}{"═" * 60}')
        print(f'{Colors.BOLD}  ⚡ Dual Boost Campaign (Views + Likes){Colors.RESET}')
        print(f'{Colors.PRIMARY}{"═" * 60}{Colors.RESET}\n')
        
        video_id = self.bypass_check_video_id(tiktok_url)
        if not video_id:
            print(f'{Colors.ERROR}  ✗  Could not extract video ID{Colors.RESET}')
            return False
        
        print(f'{Colors.SUCCESS}  ✓  Video ID: {Colors.TEXT}{video_id}{Colors.RESET}')
        print(f'{Colors.DIM}  Target: {boost_count} each\n{Colors.RESET}')
        
        successful_views = 0
        successful_likes = 0
        failed_boosts = 0
        
        for boost_num in range(1, boost_count + 1):
            print(f'\n{Colors.TEXT}  Dual Boost #{boost_num}{Colors.RESET}')
            
            # Views
            print(f'{Colors.SECONDARY}  → Views{Colors.RESET}')
            if self.bypass_check_service(video_id, 229):
                views_result = self.bypass_place_order(tiktok_url, video_id, 229)
                if views_result['success']:
                    successful_views += 1
                    print(f'{Colors.SUCCESS}    ✓  Views boosted{Colors.RESET}')
                else:
                    failed_boosts += 1
                    print(f'{Colors.WARNING}    ⚠  Views failed{Colors.RESET}')
            
            time.sleep(random.uniform(2, 4))
            
            # Likes
            print(f'{Colors.ACCENT}  → Likes{Colors.RESET}')
            if self.bypass_check_service(video_id, 232):
                likes_result = self.bypass_place_order(tiktok_url, video_id, 232)
                if likes_result['success']:
                    successful_likes += 1
                    print(f'{Colors.SUCCESS}    ✓  Likes boosted{Colors.RESET}')
                else:
                    failed_boosts += 1
                    print(f'{Colors.WARNING}    ⚠  Likes failed{Colors.RESET}')
            
            total_success = successful_views + successful_likes
            total_attempts = boost_num * 2
            rate = (total_success / total_attempts * 100) if total_attempts > 0 else 0
            
            print(f'{Colors.DIM}  Views: {successful_views} | Likes: {successful_likes} | Rate: {rate:.1f}%{Colors.RESET}')
            
            if boost_num < boost_count:
                delay = random.uniform(8, 15)
                print(f'{Colors.DIM}  Next in {delay:.1f}s...{Colors.RESET}')
                time.sleep(delay)
        
        print(f'\n{Colors.PRIMARY}{"═" * 60}')
        print(f'{Colors.SUCCESS}  ✓  Dual Campaign Complete!{Colors.RESET}')
        print(f'{Colors.TEXT}  Views: {successful_views} | Likes: {successful_likes} | Failed: {failed_boosts}{Colors.RESET}')
        print(f'{Colors.PRIMARY}{"═" * 60}{Colors.RESET}\n')
        
        return True

def print_menu():
    print(f'\n{Colors.DIM}{"─" * 60}{Colors.RESET}')
    print(f'{Colors.TEXT}  Select Campaign Type:{Colors.RESET}\n')
    print(f'{Colors.PRIMARY}  [1]{Colors.RESET} Views Boost')
    print(f'{Colors.ACCENT}  [2]{Colors.RESET} Likes Boost')
    print(f'{Colors.SECONDARY}  [3]{Colors.RESET} Dual Boost (Views + Likes)')
    print(f'\n{Colors.WARNING}  [4]{Colors.RESET} Configure Settings')
    print(f'{Colors.ERROR}  [5]{Colors.RESET} Exit')
    print(f'{Colors.DIM}{"─" * 60}{Colors.RESET}')

def main():
    booster = TikTokUnlimitedBooster()
    boost_count = 100
    
    while True:
        print_header()
        print_menu()
        
        choice = input(f'\n{Colors.PRIMARY}  ➤  {Colors.RESET}').strip()
        
        if choice == '5':
            print(f'\n{Colors.SUCCESS}  ✓  Thank you for using TikTok Boost Studio{Colors.RESET}\n')
            break
        
        if choice == '4':
            try:
                new_count = int(input(f'\n{Colors.TEXT}  Enter boost count (1-9999): {Colors.RESET}').strip())
                if 1 <= new_count <= 9999:
                    boost_count = new_count
                    print(f'{Colors.SUCCESS}  ✓  Updated to {boost_count}{Colors.RESET}')
                else:
                    print(f'{Colors.ERROR}  ✗  Invalid range{Colors.RESET}')
            except ValueError:
                print(f'{Colors.ERROR}  ✗  Invalid number{Colors.RESET}')
            time.sleep(2)
            continue
        
        if choice not in ('1', '2', '3'):
            print(f'{Colors.ERROR}  ✗  Invalid choice{Colors.RESET}')
            time.sleep(2)
            continue
        
        print(f'\n{Colors.TEXT}  Enter TikTok URL:{Colors.RESET}')
        tiktok_url = input(f'{Colors.PRIMARY}  ➤  {Colors.RESET}').strip()
        
        if not tiktok_url or 'tiktok.com' not in tiktok_url:
            print(f'{Colors.ERROR}  ✗  Invalid URL{Colors.RESET}')
            time.sleep(2)
            continue
        
        if choice == '1':
            booster.unlimited_boost_views(tiktok_url, boost_count)
        elif choice == '2':
            booster.unlimited_boost_likes(tiktok_url, boost_count)
        elif choice == '3':
            booster.dual_boost_views_likes(tiktok_url, boost_count)
        
        input(f'\n{Colors.DIM}Press Enter to continue...{Colors.RESET}')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f'\n{Colors.WARNING}  ⚠  Program interrupted{Colors.RESET}\n')
    except Exception as e:
        print(f'\n{Colors.ERROR}  ✗  Error: {e}{Colors.RESET}\n')