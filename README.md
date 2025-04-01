**README - Endpoint Extractor Tool**


### **Description**
This tool is particularly powerful during the **endpoint enumeration phase** of reconnaissance, especially when analyzing open-source software (e.g., CMS platforms, web apps like "Open Source CME," or self-hosted tools). Here’s how it fits into your workflow:

---

### **Use Case: Open-Source Software Analysis**  
1. **Scenario**: You discover an open-source application (e.g., a CMS or API framework) deployed in a target environment.  
2. **Goal**: Map all possible endpoints (URLs and internal file paths) to identify:  
   - Hidden API routes  
   - Admin interfaces  
   - Configuration files  
   - Debug endpoints  
   - Sensitive file exposures (e.g., `config.json`, `backup.sql`)  

---

### **Why This Tool Shines**  
- **Source Code Advantage**: Directly parse the project’s source code to extract endpoints that may not be visible in live deployments (e.g., internal APIs, debug routes).  
- **Speed**: Multithreaded scanning processes hundreds of files in seconds.  
- **Accuracy**: Normalizes URLs (e.g., `http://example.com/admin/` → `admin/`) and retains file paths (e.g., `src/database/credentials.php`).  

---

### **Features**  
- Scans files recursively in a directory.  
- Extracts URLs and normalizes them into endpoint paths.  
- Includes relative file paths as endpoints.  
- Removes duplicate entries.  
- Multithreaded processing for speed.  
- Progress bar visualization.  
- Output to console or file.  

---

### **Requirements**  
- Python 3.6+  
- `tqdm` package (for progress bars).  
- `grep` installed and available in PATH (see notes below).  

---

### **Installation**  
1. **Install Python Dependencies**:  
   ```bash
   pip install tqdm
   ```  
2. Ensure `grep` is installed (usually pre-installed on Linux/macOS).  

---

### **Usage**  
```bash
python endpoint_extractor.py [FOLDER] [-o OUTPUT_FILE]
```  

- **`[FOLDER]`**: Path to the folder to scan.  
- **`-o OUTPUT_FILE`** (Optional): Save results to a file.  

**Example**:  
```bash
python endpoint_extractor.py ./my_project -o endpoints.txt
```  

---

### **Example Output for Open Source CME**  
If analyzing a project like **"Open Source CME"**, the tool might extract:  
```plaintext
admin/api/users
config/database.yml  
src/utils/debug.php  
login?redirect=admin  
```

These endpoints could reveal:  
- Admin API access  
- Database credentials  
- Debug utilities  
- Authentication bypass risks  

--- 

### **Notes**  
1. **Encoding Issues**: If encountering encoding errors, modify the `open()` function in the code to use `utf-8-sig` instead of `utf-8`.  
---

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

---
