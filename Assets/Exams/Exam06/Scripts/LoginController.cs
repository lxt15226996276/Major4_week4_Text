using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
namespace Exam.Exam06
{
    /// <summary>
    /// 登录：面板互斥 字典注册/登录 成功进Loading
    /// </summary>
    public class LoginController : MonoBehaviour
    {
        [Header("面板")]
        [SerializeField] private GameObject initialPanel;
        [SerializeField] private GameObject loginPanel;
        [SerializeField] private GameObject registerPanel;

        [Header("Initial")]
        [SerializeField] private Button btnToLogin;
        [SerializeField] private Button btnToRegister;

        [Header("Login")]
        [SerializeField] private InputField loginAccount;
        [SerializeField] private InputField loginPassword;
        [SerializeField] private Button btnLogin;
        [SerializeField] private Button btnBackLogin;

        [Header("Register")]
        [SerializeField] private InputField registerAccount;
        [SerializeField] private InputField registerPassword;
        [SerializeField] private Button btnRegister;
        [SerializeField] private Button btnBackRegister;

        private AccountData _accountData = new AccountData();

        void Start()
        {
            ShowPanel(initialPanel);
            btnToLogin.onClick.AddListener(() => ShowPanel(loginPanel));
            btnToRegister.onClick.AddListener(() => ShowPanel(registerPanel));
            btnLogin.onClick.AddListener(OnLogin);
            btnRegister.onClick.AddListener(OnRegister);
            btnBackRegister.onClick.AddListener(() => ShowPanel(initialPanel));
            btnBackLogin.onClick.AddListener(() => ShowPanel(initialPanel));

        }
        /// <summary>
        /// 注册
        /// </summary>
        private void OnRegister()
        {
            if (!_accountData.Register(registerAccount.text, registerPassword.text, out string msg))
            {
                Debug.Log(msg);
                return;
            }
            Debug.Log(msg);
            ShowPanel(loginPanel);
        }

        /// <summary>
        /// 登录
        /// </summary>
        private void OnLogin()
        {
            if (!_accountData.TryLogin(loginAccount.text, loginPassword.text, out string msg))
            {
                Debug.Log(msg);
                return;
            }
            Debug.Log(msg);
            SceneManager.LoadScene(SceneNames.Loading);
        }
        /// <summary>
        /// 互斥显示一个面板
        /// </summary>
        private void ShowPanel(GameObject panel)
        {
            loginPanel.SetActive(panel == loginPanel);
            registerPanel.SetActive(panel == registerPanel);
            initialPanel.SetActive(panel == initialPanel);
        }
        private void OnDestroy()
        {
            btnToLogin.onClick.RemoveAllListeners();
            btnToRegister.onClick.RemoveAllListeners();
            btnLogin.onClick.RemoveListener(OnLogin);
            btnRegister.onClick.RemoveListener(OnRegister);
            btnBackRegister.onClick.RemoveAllListeners();
            btnBackLogin.onClick.RemoveAllListeners();
        }
    }

}
