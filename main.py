import hashlib
import toml
from bs4 import BeautifulSoup
import re

# 無效文字清單，用於排除不相關的項目
INVALID_TEXTS = {
    "使用條款", "使用說明", "個人檔案", "地點", "工作機會", "已標註", "探索探索",
    "搜尋搜尋", "新貼文建立", "聯絡人上傳和非用戶", "設定更多", "貼文", "通知通知",
    "連續短片連續短片", "部落格", "關於", "隱私", "首頁首頁"
}

# 驗證是否為有效帳號名稱的正則表達式
USERNAME_REGEX = re.compile(r'^[a-z0-9._]+$')


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
        # 假設帳號名稱在 <a> 標籤中，過濾無效文字和非帳號格式的項目
        usernames = set(
            a.text.strip() for a in soup.select('a')
            if a.text and a.text.strip() not in INVALID_TEXTS and USERNAME_REGEX.match(a.text.strip())
        )
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
        "followers": {
            "count": len(followers_list),
            "accounts": followers_list,
        },
        "following": {
            "count": len(following_list),
            "accounts": following_list,
        },
        "not_followed_back": {
            "count": len(not_followed_back),
            "accounts": not_followed_back,
        },
        "not_following_back": {
            "count": len(not_following_back),
            "accounts": not_following_back,
        },
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        toml.dump(data, f)

    print(f"結果已輸出到 {output_file}")
