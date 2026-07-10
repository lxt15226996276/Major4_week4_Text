using UnityEngine;
using UnityEngine.UI;


namespace Exam.Exam01
{
    public class MainUIController : MonoBehaviour
    {
        [SerializeField] private Button _btnBag;
        [SerializeField] private Button _btnSkill;
        [SerializeField] private Button _btnCloseBag;
        [SerializeField] private Button _btnCloseSkill;
        [SerializeField] private GameObject _bagPanel;
        [SerializeField] private GameObject _skillPanel;

        void Start()
        {
            _btnBag.onClick.AddListener(() => ShowPanel(_bagPanel));
            _btnSkill.onClick.AddListener(() => ShowPanel(_skillPanel));

            _btnCloseBag.onClick.AddListener(() => _bagPanel.SetActive(false));
            _btnCloseSkill.onClick.AddListener(() => _skillPanel.SetActive(false));
        }

        /// <summary>
        /// 显示面板
        /// </summary>
        private void ShowPanel(GameObject panel)
        {
            _bagPanel.SetActive(_bagPanel == panel);
            _skillPanel.SetActive(_skillPanel == panel);
        }

    }
}

