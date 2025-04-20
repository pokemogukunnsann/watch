from flask import Flask, request, Response
import subprocess
from bs4 import BeautifulSoup

app = Flask(__name__)

INVIDIOUS_INSTANCES = [
    "https://cal1.iv.ggtyler.dev", "https://lekker.gay", "https://pol1.iv.ggtyler.dev",
    "https://iv.melmac.space", "https://nyc1.iv.ggtyler.dev", "https://invidious.lunivers.trade",
    "https://iv.ggtyler.dev", "https://eu-proxy.poketube.fun", "https://invidious.f5.si",
    "https://invidious.reallyaweso.me", "https://invidious.dhusch.de", "https://yewtu.be",
    "https://usa-proxy2.poketube.fun", "https://id.420129.xyz", "https://invidious.materialio.us",
    "https://invidious.darkness.service", "https://iv.datura.network", "https://invidious.jing.rocks",
    "https://invidious.private.coffee", "https://youtube.mosesmang.com", "https://invidious.projectsegfau.lt",
    "https://invidious.perennialte.ch", "https://invidious.einfachzocken.eu", "https://invidious.adminforge.de",
    "https://iv.duti.dev", "https://invid-api.poketube.fun", "https://inv.nadeko.net",
    "https://invidious.esmailelbob.xyz", "https://invidious.0011.lt", "https://invidious.ducks.party",
    "https://invidious.privacyredirect.com", "https://youtube.privacyplz.org", "https://yt.artemislena.eu",
    "https://invidious.schenkel.eti.br"
]

@app.route('/watch')
def watch_video():
    videoid = request.args.get('v')
    
    url = f'https://www.youtube.com/watch?v={videoid}'
    curl_command = ['curl', '-s', url]
    
    try:
        result = subprocess.check_output(curl_command)
        html_content = result.decode('utf-8')

        soup = BeautifulSoup(html_content, 'html.parser')

        # #player を探してiframeに置き換える
        player_div = soup.find(id='player')
        if player_div:
            # 差し替え用iframeタグ作成
            iframe = soup.new_tag("iframe")
            iframe['src'] = f'https://www.youtubeeducation.com/embed/{videoid}?embed_config=%7B%22enc%22%3A%22AXH1ezkRiBJkmX6qs8WHisUf72KwPPjLRshwQcdT1lv-pDgxChnF5o4Oi692Y-DeUTO4Y5atxHwwp_P1H7usZTpc7tVgZ_wg0XJ5l8H5YBY1GFcI0kcGVoFoj64vhmZS-dzfjOw7u_9J9LFZejoQ_Ow_R-MuqRkfJQ%3D%3D%22%2C%22hideTitle%22%3Atrue%7D'
            iframe['allowfullscreen'] = ''
            iframe['width'] = '640'
            iframe['height'] = '360'
            iframe['frameborder'] = '0'

            # 置き換え
            player_div.clear()
            player_div.append(iframe)

            return Response(str(soup), mimetype='text/html')
        else:
            return "プレイヤーが見つかりません"

    except subprocess.CalledProcessError as e:
        return f"Error fetching YouTube page: {e}"

@app.route('/comments')
def get_comments():
    videoid = request.args.get('v')
    if not videoid:
        return jsonify({'error': '動画ID (v) が必要です'}), 400

    instance = random.choice(INVIDIOUS_INSTANCES)
    url = f"{instance}/api/v1/comments/{videoid}"

    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        comments = res.json()
        return jsonify(comments)
    except Exception as e:
        return jsonify({'error': 'Invidiousからコメント取得に失敗しました', 'details': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
