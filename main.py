from flask import Flask, request, Response
import subprocess

app = Flask(__name__)

@app.route('/watch')
def watch_video():
    videoid = request.args.get('v')  # URLの?後のvideoidを取得
    
    # YouTubeのURLを取得するためのcurlコマンド
    url = f'https://www.youtube.com/watch?v={videoid}'
    curl_command = ['curl', '-s', url]
    
    # curlコマンドでYouTubeページを取得
    try:
        result = subprocess.check_output(curl_command)
        html_content = result.decode('utf-8')
        
        # 動画再生部分のHTMLに置き換える
        video_html = f'''
        <video controls="" autoplay="" poster="https://img.youtube.com/vi/{videoid}/0.jpg" width="640" height="360">
            <source src="https://inv-eu2-c.nadeko.net/api/manifest/dash/id/QJo9X5riyWE?local=true&unique_res=1&check=" type="application/dash+xml" label="dash">
            <source src="https://inv-ca1-c.nadeko.net/latest_version?id={videoid}&itag=18&check=" type="video/mp4">
            <source src="https://inv-us2-c.nadeko.net/latest_version?id={videoid}&itag=18&check=" type="video/mp4">
            <source src="https://inv-eu2-c.nadeko.net/latest_version?id={videoid}&itag=18&check=" type="video/mp4">
            <source src="https://inv-eu3-c.nadeko.net/latest_version?id={videoid}&itag=18&check=" type="video/mp4">
            お使いのブラウザは動画タグをサポートしていません。
        </video>
        '''
        
        # 受け取ったHTMLを変更してレスポンスを返す
        return Response(video_html, mimetype='text/html')
    
    except subprocess.CalledProcessError as e:
        return f"Error fetching YouTube page: {e}"

if __name__ == '__main__':
    app.run(debug=True)
