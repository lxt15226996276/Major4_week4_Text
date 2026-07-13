using System.IO.Compression;
using System.Net;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.UI;
namespace Exam.Exam06
{
    public class GameUIController : MonoBehaviour
    {
        [Header("人物面板")]
        [SerializeField] private GameObject playerInfoPanel;
        [SerializeField] private Button btnPlayerInfo;
        //[SerializeField] private Button btnClsoeInfo;

        [Header("商城")]
        [SerializeField] private GameObject shopPanel;
        [SerializeField] private Button btnShop;
        [SerializeField] private Button btnCloseShop;
        [SerializeField] private Text texGold;
        [SerializeField] private Button btnBuyGold100;
        [SerializeField] private Button btnBuyGold200;
        [SerializeField] private Button btnBuyGold300;
        [SerializeField] private Button btnBuyGold400;

        private int _gold = 1000;



        void Start()
        {
            btnPlayerInfo.onClick.AddListener(OpenPlayerInfo);
            shopPanel.SetActive(false);
            RefreshGold();
            btnShop.onClick.AddListener(() => shopPanel.SetActive(true));
            btnCloseShop.onClick.AddListener(() => shopPanel.SetActive(false));
            btnBuyGold100.onClick.AddListener(() => AddGold(100));
            btnBuyGold200.onClick.AddListener(() => AddGold(200));
            btnBuyGold300.onClick.AddListener(() => AddGold(300));
            btnBuyGold400.onClick.AddListener(() => AddGold(400));
        }
        /// <summary>
        /// 购买金币道具：增加对应金币并刷新Text
        /// </summary>
        /// <param name="amout"></param>
        private void AddGold(int amout)
        {
            _gold += amout;
            RefreshGold();
            Debug.Log($"购买成功，金币+{amout}");

        }
        /// <summary>
        /// 刷新文本
        /// </summary>
        private void RefreshGold()
        {
            texGold.text = $"金币：{_gold}";
        }
        /// <summary>
        /// 打开人物面板信息
        /// </summary>
        private void OpenPlayerInfo()
        {
            playerInfoPanel.SetActive(true);
        }

        void OnDestroy()
        {
            btnPlayerInfo.onClick.RemoveListener(OpenPlayerInfo);
        }

    }
}

