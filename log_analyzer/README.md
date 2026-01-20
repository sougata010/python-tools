# 📊 Log Analyzer

This tool is built using:

- File I/O  
- `pandas`  
- `defaultdict`  
- `functools.reduce`  

It is designed to analyze server log files and detect suspicious activity based on **IP request frequency**.

The analyzer works by:

- Reading static log files  
- Tracking each IP using a hashmap  
- Measuring how frequently an IP sends requests  
- Classifying behavior based on timing patterns  

Detection logic:

- If the **average time between requests is < 0.2s**  
  and **≥ 10 requests** are sent in that window → marked as **Bot / DDoS**  
- If requests fall in the **0.2s – 1.0s** range → the analyzer holds and forwards the IP to the next control layer  
- The next layer checks whether the IP is requesting **abnormally large amounts of data**  
- If confirmed, the IP can be **banned or rate-limited**

Currently, this tool works on **static log files**, but it is designed to be easily extended:

- Can be adapted for **real-time production systems**  
- Can integrate with tools like **Redis**, message queues, or firewalls  
- Can be part of a full **intrusion detection pipeline**

This project helps learners understand:

- How log analysis works in real systems  
- How bots and DDoS patterns are detected  
- How Python can be used to build security tooling  
- How raw logs turn into actionable security decisions  

It’s a practical bridge between **Python basics** and **real-world cybersecurity systems**.
