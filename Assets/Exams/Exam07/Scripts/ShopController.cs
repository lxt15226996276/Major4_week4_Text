using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
namespace Exam.Exam07
{
    /// <summary>
    /// 商城开关 shopPanel 金币购买HP/MP 刷线Slider/Text
    /// </summary>
    public class ShopController : MonoBehaviour
    {
        [Header("面板")]
        [SerializeField] private GameObject shopPanel;
        [SerializeField] private Button btnShop;
        [SerializeField] private Button btnClose;

        [Header("购买")]
        [SerializeField] private Button btnBuyHp;
        [SerializeField] private Button btnBuyMp;

        [Header("UI")]
        [SerializeField] private Text textGold;
        [SerializeField] private Slider sliderHp;
        [SerializeField] private Slider sliderMp;
        [SerializeField] private Text textHp;
        [SerializeField] private Text textMp;

        [Header("数值")]
        [SerializeField] private int hpPotionCost = 100;
        [SerializeField] private int mpPotionCost = 100;
        [SerializeField] private float hpRestore = 20f;
        [SerializeField] private float mpRestore = 20f;

        private int _gold = 1000;

        void Start()
        {
            // 思路：初始关商城 · 注册四个按钮 · 同步 UI
            shopPanel.SetActive(false);
            btnShop.onClick.AddListener(OpenShopPanel);
            btnClose.onClick.AddListener(ClsoeShopPanel);
            btnBuyHp.onClick.AddListener(BuyHp);
            btnBuyMp.onClick.AddListener(BuyMp);
            RefreshUI();
        }
        /// <summary>
        /// 打开商城面板
        /// </summary>
        private void OpenShopPanel()
        {
            shopPanel.SetActive(true);
        }

        /// <summary>
        /// 关闭商城面板
        /// </summary>
        private void ClsoeShopPanel()
        {
            shopPanel.SetActive(false);
        }

        /// <summary>
        /// 消耗金币回血
        /// </summary>
        private void BuyHp()
        {
            if (_gold < hpPotionCost)
            {
                Debug.Log("购买失败");
                return;
            }
            _gold -= hpPotionCost;
            sliderHp.value = Mathf.Min(sliderHp.maxValue, sliderHp.value + hpRestore);
            RefreshUI();
            Debug.Log("购买成功");
        }

        /// <summary>
        /// 消耗金币回蓝
        /// </summary>
        private void BuyMp()
        {
            if (_gold < mpPotionCost)
            {
                Debug.Log("购买失败");
                return;
            }
            _gold -= mpPotionCost;
            sliderMp.value = Mathf.Min(sliderMp.maxValue, sliderMp.value + mpRestore);
            RefreshUI();
            Debug.Log("购买成功");
        }

        /// <summary>
        /// 统一刷新金币与HP/MP文本
        /// </summary>
        private void RefreshUI()
        {
            textGold.text = $"金币：{_gold}";

            if (textHp != null)
            {
                textHp.text = $"HP：{sliderHp.value}";
            }

            if (textMp != null)
            {
                textMp.text = $"MP：{sliderMp.value}";
            }
        }
    }

}
