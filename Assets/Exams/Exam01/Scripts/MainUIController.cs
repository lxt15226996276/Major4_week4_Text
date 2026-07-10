using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace Exam.Exam01
{
    public class MainUIController : MonoBehaviour
    {
        [SerializeField] private Button _btnBag;
        [SerializeField] private Button _btnSkill;
        [SerializeField] private GameObject _bagPanel;
        [SerializeField] private GameObject _skillPanel;

        void Start()
        {
            _btnBag.onClick.AddListener(() => ShowPanel(_bagPanel));
            _btnSkill.onClick.AddListener(() => ShowPanel(_skillPanel));
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

