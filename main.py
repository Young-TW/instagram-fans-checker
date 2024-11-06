import hashlib
import toml
from bs4 import BeautifulSoup

# 計算檔案的哈希值以檢查是否相同
def get_file_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        buf = file.read()
        hasher.update(buf)
    return hasher.hexdigest()

# 讀取 HTML 檔案並解析帳號名稱
def extract_usernames_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        # 假設帳號名稱在 <a> 標籤中，這裡的選擇器根據實際情況進行調整
        usernames = set(a.text for a in soup.select('a') if a.text)
    return usernames

# 設定檔案路徑
followers_file = 'followers.html'
following_file = 'following.html'
output_file = 'instagram_relationships.toml'

# 比較兩個檔案是否相同
followers_hash = get_file_hash(followers_file)
following_hash = get_file_hash(following_file)

if followers_hash == following_hash:
    print("兩個檔案內容相同，無需比對。")
else:
    print("檔案不同，開始解析並比對帳號。")

    # 解析 followers 和 following 檔案
    followers = extract_usernames_from_html(followers_file)
    following = extract_usernames_from_html(following_file)

    # 計算四個列表
    followers_list = sorted(followers)
    following_list = sorted(following)
    not_following_back = sorted(following - followers)
    not_followed_back = sorted(followers - following)

    # 將結果寫入 .toml 檔案
    data = {
        "followers": followers_list,
        "following": following_list,
        "not_followed_back": not_followed_back,      # 粉絲但未回追
        "not_following_back": not_following_back,    # 追蹤但對方未回追
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        toml.dump(data, f)

    print(f"結果已輸出到 {output_file}")
