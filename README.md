## Syscall-IDS

Host-based Intrusion Detection System (HIDS) that identifies anomalies in system call traces by leveraging a combination of statistical methods and machine learning algorithms to distinguish between normal (clean) and potentially malicious (infected) process behaviors.

View pipeline <a href="https://github.com/Vismay-dev/SysCall-IDS/blob/main/notebooks/subcom_pipeline.ipynb" target="_blank">here</a>.

### 🌟 Key Developments

| Technique/Feature                   | Description                                                                     |
|-------------------------------------|---------------------------------------------------------------------------------|
| Feature Engineering                 | Conversion of syscall info into high-dimensional feature vectors.               |
| Probabilistic Syscall Subclustering | Gaussian Mixture Models for granular syscall behavior understanding.            |
| Temporal Dependency Modeling        | Markov Chains capture transitions between syscall states as a function of time. |
| Buffer Overflow Detection           | Gaussian interval of string argument lengths to catch overflow attempts.        |
| Pathname Similarity Analysis        | SOMs to visualize and detect anomalies in syscall pathnames.                    |
| DoS Attack Detection                | Markov Chain edge frequency analysis per-trace for DoS detection.                |

### 🎓 References:

- <a href="https://maggi.cc/publication/frossi_hybridsyscalls_2009/frossi_hybridsyscalls_2009.pdf" target="_blank">Frossi et al. "Selecting and Improving System Call Models for Anomaly Detection"</a>
- <a href="https://ieeexplore.ieee.org/document/9796248" target="_blank">Android Dataset</a>

### 🙏 Acknowledgments:

- <a href="http://ids.cs.columbia.edu/sites/default/files/smt-syscall-discex01.pdf" target="_blank">Columbia CS Dept's Intrusion Detection Pipeline</a>
- <a href="http://bactra.org/notebooks/prediction-process.html" target="_blank">Cosma Shalizi's Notes on Markov Chains and Prediction Processes</a>

## 📝 License

This project is licensed under the <a href="https://www.gnu.org/licenses/agpl-3.0.en.html" target="_blank">GNU Affero General Public License v3.0</a>.
