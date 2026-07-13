using System.Collections.Generic;
namespace Exam.Exam06
{
    /// <summary>
    /// 账号数据 Dictionary 存账号密码 注册与登录校验
    /// </summary>
    public class AccountData
    {
        private readonly Dictionary<string, string> _accounts = new Dictionary<string, string>();

        /// <summary>
        /// 注册：账号不存在则写入字典
        /// </summary>
        /// <returns></returns>
        public bool Register(string account, string password, out string message)
        {
            account = account?.Trim();
            password = password?.Trim();

            if (string.IsNullOrEmpty(account) || string.IsNullOrEmpty(password))
            {
                message = "账号或密码不能为空";
                return false;
            }

            if (_accounts.ContainsKey(account))
            {
                message = "账号已存在";

                return false;
            }

            _accounts.Add(account, password);
            message = "注册成功";
            return true;
        }

        /// <summary>
        /// 登录
        /// </summary>
        /// <returns></returns>
        public bool TryLogin(string account, string password, out string message)
        {
            account = account?.Trim();
            password = password?.Trim();

            if (!_accounts.TryGetValue(account, out string stored))
            {
                message = "账号未注册";
                return false;
            }

            if (password != stored)
            {
                message = "密码错误";
                return false;
            }

            message = "登录成功";
            return true;
            //return _accounts.TryGetValue(account, out string stored) && stored == password;
        }
    }
}

