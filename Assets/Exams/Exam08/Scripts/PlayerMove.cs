using UnityEngine;

namespace Exam.Exam08
{
    /// <summary>
    /// player移动 cc+2d混合
    /// </summary>
    [RequireComponent(typeof(CharacterController))]
    [RequireComponent(typeof(Animator))]
    public class PlayerMove : MonoBehaviour
    {
        [SerializeField] private float moveSpeed = 3.5f;
        [SerializeField] private float animDampTime = 0.1f;
        [SerializeField] private CharacterController _controller;
        [SerializeField] private Animator _animator;

        private readonly int VelocityXHash = Animator.StringToHash("VelocityX");
        private readonly int VelocityZHash = Animator.StringToHash("VelocityZ");

        void Awake()
        {
            _animator = GetComponent<Animator>();
            _controller = GetComponent<CharacterController>();
        }

        void Update()
        {
            float h = Input.GetAxisRaw("Horizontal");
            float v = Input.GetAxisRaw("Vertical");

            Vector3 raw = new Vector3(h, 0, v);
            bool isMoving = raw.sqrMagnitude > 0.1f;

            if (isMoving)
            {
                Vector3 dic = raw.normalized;
                _controller.Move(dic * moveSpeed * Time.deltaTime);
            }

            _animator.SetFloat(VelocityXHash, h, animDampTime, Time.deltaTime);
            _animator.SetFloat(VelocityZHash, v, animDampTime, Time.deltaTime);
        }
    }
}

