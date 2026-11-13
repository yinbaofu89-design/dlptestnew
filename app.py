import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="DLP Test", layout="wide")

HTML = r"""
<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<style>
 body{font-family:sans-serif;margin:16px;color:#222}
 label{display:block;margin-top:14px;font-weight:bold}
 select,input[type=text],textarea{width:100%;padding:6px;box-sizing:border-box}
 button{margin-top:16px;padding:8px 24px;background:#d33;color:#fff;border:0;border-radius:6px;font-size:15px;cursor:pointer}
 #msg{margin-top:16px;padding:10px;border-radius:6px;display:none}
 .ok{background:#e6f4ea;color:#137333}.ng{background:#fce8e6;color:#c5221f}.info{background:#e8f0fe;color:#1a56c4}
 pre{white-space:pre-wrap;word-break:break-all;background:#f5f5f5;padding:8px;max-height:300px;overflow:auto}
</style></head><body>
<h2>DLP テストページ</h2>
<form id="f" method="post" enctype="multipart/form-data" target="_self">
 <label>送信先URL</label>
 <select id="url">
  <option selected>https://httpbin.org/post</option>
  <option>https://postman-echo.com/post</option>
  <option>https://httpbingo.org/post</option>
  <option>https://dlptest.com/api/http-post/</option>
 </select>
 <label>任意URL（入力時はこちらを優先）</label>
 <input type="text" id="custom">
 <label>テキスト</label>
 <textarea name="text" id="text" rows="6"></textarea>
 <label>ファイル</label>
 <input type="file" name="file" id="file">
 <br><button type="button" id="send">送信</button>
</form>
<div id="msg"></div>
<pre id="body" style="display:none"></pre>
<script>
const KEYS=["Access Denied","content_filter_denied","Transaction ID:"];
const $=id=>document.getElementById(id);
function show(cls,t){const m=$("msg");m.className=cls;m.textContent=t;m.style.display="block";}
$("send").onclick=async()=>{
  const url=$("custom").value.trim()||$("url").value;
  const fd=new FormData();
  fd.append("text",$("text").value);
  if($("file").files[0]) fd.append("file",$("file").files[0]);
  $("body").style.display="none";
  show("info","送信中...");
  try{
    const r=await fetch(url,{method:"POST",body:fd});
    const t=await r.text();
    if(KEYS.some(k=>t.includes(k))){document.open();document.write(t);document.close();return;}
    show(r.ok?"ok":"ng",(r.ok?"正常に送信しました":"送信失敗")+"（HTTP "+r.status+"）");
    $("body").textContent=t.slice(0,3000);$("body").style.display="block";
  }catch(e){
    // 応答を読めない場合（例外ページ等）はフォーム送信し、画面全体を応答に置き換える
    const f=$("f");f.action=url;f.submit();
  }
};
</script></body></html>
"""

components.html(HTML, height=1100, scrolling=True)
