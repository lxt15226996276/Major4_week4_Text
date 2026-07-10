using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
namespace Exam.Exam01
{
    public class LoginController : MonoBehaviour
    {
        [Header("UI 引用")]
        [SerializeField] private InputField _inputAccount;
        [SerializeField] private InputField _inputPassword;
        [SerializeField] private Button _btnLogin;

        private readonly Dictionary<string, string> _accountDic = new Dictionary<string, string>();

        void Awake()
        {
            _accountDic.Add("lixiaotong", "123456");
        }

        void Start()
        {
            _btnLogin.onClick.AddListener(OnLoginClick);
        }

        /// <summary>
        /// 登录验证
        /// </summary>
        private void OnLoginClick()
        {
            string account = _inputAccount.text.Trim();
            string password = _inputPassword.text.Trim();

            if (!_accountDic.TryGetValue(account, out string stored) || stored != password)
            {
                Debug.Log("账号不存在或密码错误");
                _inputAccount.text = null;
                _inputPassword.text = null;
                _inputAccount.ActivateInputField();
                return;
            }
            Debug.Log("登录成功");
            SceneManager.LoadScene(SceneNames.Main);
        }

        void OnDestroy()
        {
            _btnLogin.onClick.RemoveListener(OnLoginClick);
        }
    }

}

