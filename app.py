from flask import Flask, render_template, request, redirect, url_for, session
import ollama
from nltk.tokenize import sent_tokenize
import pymupdf as pdf
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
import pymysql as sql
import os
from werkzeug.utils import secure_filename
import easyocr
import cv2
app = Flask(__name__)
app.secret_key = "supersecretkey"
collection_name='kvkrag'
chroma_db_path=r'C:\Users\kumar\Desktop\KVKDEV\Hacknovation2.0\db'
UPLOAD_FOLDER=r'C:\Users\kumar\Desktop\KVKDEV\Hacknovation2.0\static\files'
documents=[]
ids=[]
metadatas=[]
counter=0
uploaded_files=[]
reader = easyocr.Reader(['en'], gpu=False)
conn=sql.connect(host='localhost',user='root',password='',database='syllobot')
curs=conn.cursor()
chroma_client=chromadb.PersistentClient(path=chroma_db_path)
embedding_function=DefaultEmbeddingFunction()
try:
    chroma_client.delete_collection(name=collection_name)
except:
    pass
collection=chroma_client.create_collection(name=collection_name,embedding_function=embedding_function)
def chunking(page_text,max_words=500):
    sents=sent_tokenize(page_text)
    chunks=[]
    current_chunk=[]
    current_length=0
    for sentence in sents:
        words=sentence.split()
        word_count=len(words)
        if len(words)<8: continue
        if current_length+word_count<=max_words:
            current_chunk.append(sentence)
            current_length+=word_count
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk=[sentence]
            current_length=word_count
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks
def generate(question):
    results=collection.query(query_texts=[question],n_results=3)
    if not results["documents"] or not results["documents"][0]:
        return "No relevant documents found."
    retrieved_chunks=results["documents"][0]
    context="\n\n".join(retrieved_chunks)
    prompt=f"""You are a AI Based Student Doubt solving system.
Use ONLY the provided context.
If answer not found say "Not found in document."
Context:{context}
Question:{question}
Answer:"""
    response=ollama.chat(
        model='qwen2.5:0.5b',
        messages=[{"role":"user","content":prompt}],
        stream=False,
        options={"num_predict":200}
    )
    return response['message']['content']
def generate_image_model(question):
    prompt=f"""You are an AI that solves questions extracted from images.
Answer clearly and directly.
If unclear, say you cannot understand properly.
Question:
{question}
Answer:"""
    response=ollama.chat(
        model='qwen2.5:0.5b',
        messages=[{"role":"user","content":prompt}],
        stream=False,
        options={"num_predict":300}
    )
    return response['message']['content']
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login_page')
def login_page():
    return render_template('login.html')
@app.route('/signup')
def signup_page():
    return render_template('signup.html')
@app.route('/login',methods=['POST'])
def new_user():
    fname=request.form.get('fname')
    email=request.form.get('email')
    username=request.form.get('username')
    userpass=request.form.get('password')
    query='insert into user_tb values(%s,%s,%s,%s);'
    curs.execute(query,[fname,username,userpass,email])
    conn.commit()
    return render_template('login.html')
@app.route('/SyllobotAI_Home',methods=['POST'])
def authentication():
    username=request.form.get('username')
    user_pass=request.form.get('password')
    query='select * from user_tb where username=%s and userpass=%s;'
    curs.execute(query,[username,user_pass])
    dt=curs.fetchone()
    if dt:
        session['user']={'fname':dt[0],'username':dt[1]}
        return redirect(url_for('home'))
    return render_template('login.html')
@app.route('/history')
def history_page():
    if 'user' not in session:
        return redirect(url_for('login_page'))
    user = session['user']
    username = user['username']
    query = "SELECT * FROM user_dt WHERE user=%s ORDER BY idx DESC;"
    curs.execute(query, (username,))
    rows = curs.fetchall()
    timeline_items = []
    total_questions = 0
    total_uploads = 0
    for row in rows:
        idx, user, question, answer, file_name, file_type = row
        if question and answer:
            timeline_items.append({
                "type": "question",
                "question": question,
                "answer": answer,
                "time": idx,
            })
            total_questions += 1
        if file_name:
            timeline_items.append({
                "type": "upload",
                "name": file_name,
                "filetype": file_type,
                "time": idx
            })
            total_uploads += 1
    return render_template(
        "history.html",
        timeline_items=timeline_items,
        total_questions=total_questions,
        total_uploads=total_uploads,
        data=user
    )
@app.route('/Home_Syllobot')
def home():
    user=session.get('user',{'fname':'user','username':'guest'})
    return render_template('dashboard.html',data=user,uploaded_files=uploaded_files)
@app.route('/upload', methods=['POST'])
def read_file():
    global counter
    file_ip = request.files.get('file')
    upload_type = request.form.get("upload_type")
    if 'user' not in session:
        return redirect(url_for('login_page'))
    user = session['user']
    username = user['username']
    if file_ip and file_ip.filename != '':
        filename = secure_filename(file_ip.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file_ip.save(file_path)
        file_type = upload_type
        extracted_text = ""
        if file_type == "pdf":
            data = pdf.open(file_path)
            for page in data:
                extracted_text += page.get_text()
            chunks = chunking(extracted_text)
            local_ids=[]
            local_docs=[]
            local_meta=[]
            for chunk in chunks:
                local_docs.append(chunk)
                local_ids.append(str(counter))
                local_meta.append({"source": filename})
                counter+=1
            if local_docs:
                collection.add(ids=local_ids,documents=local_docs,metadatas=local_meta)
            curs.execute("""
                INSERT INTO user_dt (user,file_name,file_type)
                VALUES (%s,%s,%s);
            """,(username,filename,file_type))
            conn.commit()
        elif file_type == "image":
            img = cv2.imread(file_path)
            result = reader.readtext(img, detail=0)
            extracted_text = " ".join(result)
            if extracted_text.strip() != "":
                chunks = chunking(extracted_text)
                local_ids = []
                local_docs = []
                local_meta = []
                for chunk in chunks:
                    local_docs.append(chunk)
                    local_ids.append(str(counter))
                    local_meta.append({"source": filename})
                    counter += 1
                if local_docs:
                    collection.add(
                        ids=local_ids,
                        documents=local_docs,
                        metadatas=local_meta
                        )
                answer = generate_image_model(extracted_text)
                curs.execute("""
                             INSERT INTO user_dt (user,question,answer,file_name,file_type)
                             VALUES (%s,%s,%s,%s,%s);
                             """,
                             (username,extracted_text,answer,filename,file_type))
                conn.commit()
                messages=[
            {"type":"user","content":extracted_text,"time":"Now"},
            {"type":"bot","content":answer,"time":"Now"}
        ]
                uploaded_files.append({
            "name": filename,
            "size": str(round(os.path.getsize(file_path)/1024,2))+" KB",
            "type": file_type,
            "date": "Now"
        })
                return render_template(
            'dashboard.html',
            messages=messages,
            data=user,
            uploaded_files=uploaded_files
        )
        uploaded_files.append({
            "name": filename,
            "size": str(round(os.path.getsize(file_path)/1024,2))+" KB",
            "type": file_type,
            "date": "Now"
        })
    return render_template('dashboard.html',data=user,uploaded_files=uploaded_files)
@app.route('/ask', methods=['POST'])
def ask():
    question=request.form.get('question')
    if 'user' not in session:
        return redirect(url_for('login_page'))
    user=session['user']
    username=user['username']
    if not question:
        return render_template('dashboard.html',data=user,uploaded_files=uploaded_files)
    answer=generate(question)
    insert_query="""
        INSERT INTO user_dt (user,question,answer)
        VALUES (%s,%s,%s);
    """
    curs.execute(insert_query,(username,question,answer))
    conn.commit()
    messages=[
        {"type":"user","content":question,"time":"Now"},
        {"type":"bot","content":answer,"time":"Now"}
    ]
    return render_template('dashboard.html',messages=messages,data=user,uploaded_files=uploaded_files)
@app.route('/SyllobotLogout')
def logout():
    return render_template('login.html')
if __name__=='__main__':
    app.run(debug=True,port=2000)
