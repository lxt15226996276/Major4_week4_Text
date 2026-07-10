using Unity.VisualScripting;
using UnityEditor.Tilemaps;
using UnityEngine;
using UnityEngine.UI;

namespace Exam.Exam01
{
    public class SkillController : MonoBehaviour
    {
        [SerializeField] private Button[] _skillButtons;
        [SerializeField] private GameObject _skillPopUp;
        [SerializeField] private Text _titleText;
        [SerializeField] private Text _descText;
        [SerializeField] private Button _btnClosePropUp;

        private readonly SkillData[] _skills =
        {
            new SkillData{skillName="暗影魔法球",description="向前方发射一枚暗影能量弹，命中敌人造成伤害",animTrigger="Skill1"},
            new SkillData{skillName="暗影连弹",description="连续发射多枚暗影魔法球，进行多段远程压制 ",animTrigger="Skill2"},
            new SkillData{skillName="暗影冲击波",description="释放大范围暗影冲击波，击退周围敌人",animTrigger="Skill4"},
            new SkillData{skillName="多重暗影打击",description="召唤多道暗影能量连续打击目标区域，造成多段伤害",animTrigger="Skill6"},
        };

        void Start()
        {
            _btnClosePropUp.onClick.AddListener(ClosePopUp);
            for (int i = 0; i < _skillButtons.Length; i++)
            {
                int index = i;
                _skillButtons[i].onClick.AddListener(() => ShowSkillInfo(index));
            }
        }
        /// <summary>
        /// 显示详情面板
        /// </summary>
        /// <param name="index"></param>
        private void ShowSkillInfo(int index)
        {
            SkillData skill = _skills[index];
            _titleText.text = skill.skillName;
            _descText.text = skill.description;
            _skillPopUp.SetActive(true);
        }
        private void OnDestroy()
        {
            _btnClosePropUp.onClick.RemoveListener(ClosePopUp);
            foreach (var btn in _skillButtons)
            {
                btn.onClick.RemoveAllListeners();
            }
        }
        /// <summary>
        /// 关掉面板
        /// </summary>
        void ClosePopUp()
        {
            _skillPopUp.SetActive(false);
        }

    }

}
