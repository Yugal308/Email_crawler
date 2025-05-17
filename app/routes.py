from flask import render_template, request, jsonify, send_file
from app import app
from app.crawler import EmailCrawler
import pandas as pd
import os
from werkzeug.utils import secure_filename
import tempfile
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    logger.debug("Index route accessed")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    logger.debug("Upload route accessed")
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Please upload a CSV file'}), 400

    # Create a temporary file
    temp_dir = tempfile.mkdtemp()
    input_path = os.path.join(temp_dir, 'input.csv')
    output_path = os.path.join(temp_dir, 'results.csv')
    
    file.save(input_path)
    
    try:
        # Process the CSV
        df = pd.read_csv(input_path)
        if 'website name' not in df.columns or 'website link' not in df.columns:
            return jsonify({'error': 'CSV must contain "website name" and "website link" columns'}), 400
        
        results = []
        for index, row in df.iterrows():
            website_name = row['website name']
            website_url = row['website link']
            
            try:
                crawler = EmailCrawler()
                crawler.crawl_website(website_url)
                website_results = crawler.get_results()
                
                results.append({
                    'website_name': website_name,
                    'website_url': website_url,
                    'emails': website_results['emails'],
                    'phone_numbers': website_results['phone_numbers']
                })
            except Exception as e:
                results.append({
                    'website_name': website_name,
                    'website_url': website_url,
                    'error': str(e)
                })
        
        # Save results to CSV
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_path, index=False)
        
        return send_file(output_path, 
                        mimetype='text/csv',
                        as_attachment=True,
                        download_name='results.csv')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500 