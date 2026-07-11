using Unity.VisualScripting;
using UnityEngine;

namespace Exam.Exam01
{
    public class BagController : MonoBehaviour
    {
        [SerializeField] private GameObject itemPrefab;
        [SerializeField] private Transform contentRoot;
        private int itemCount = 20;
        void Start()
        {
            CreatItems();
        }
        private void CreatItems()
        {
            for (int i = 0; i < itemCount; i++)
            {
                Instantiate(itemPrefab, contentRoot);
            }
        }
    }
}

