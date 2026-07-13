using System.Collections;
using System.Collections.Generic;
using UnityEngine;
namespace Exam.Exam07
{
    /// <summary>
    /// Player 移动 cc+2d混合树
    /// </summary>
    [RequireComponent(typeof(CharacterController))]
    [RequireComponent(typeof(Animator))]
    public class PlayerMove : MonoBehaviour
    {
        [SerializeField] private float moveSpeed = 5f;
        [SerializeField] private float animDampTime = 0.1f;
        [SerializeField] private CharacterController _controller;
        [SerializeField] private Animator _animator;

        private readonly int VelocityXHash = Animator.StringToHash("VelocityX");
        private readonly int VelocityZHash = Animator.StringToHash("VelocityZ");

        void Awake()
        {
            _controller = GetComponent<CharacterController>();
            _animator = GetComponent<Animator>();
        }

        void Update()
        {
            //思路：读轴 判断是否移动 cc位移+转身 阻尼写入2D混合数
            float horizontal = Input.GetAxisRaw("Horizontal");
            float vertical = Input.GetAxisRaw("Vertical");

            Vector3 raw = new Vector3(horizontal, 0, vertical);
            bool isMoving = raw.sqrMagnitude > 0.01f;

            if (isMoving)
            {
                Vector3 dic = raw.normalized;
                _controller.Move(dic * moveSpeed * Time.deltaTime);

                Vector3 localMove = transform.InverseTransformDirection(dic);
                _animator.SetFloat(VelocityXHash, localMove.x, animDampTime, Time.deltaTime);
                _animator.SetFloat(VelocityZHash, localMove.z, animDampTime, Time.deltaTime);
                //transform.rotation = Quaternion.LookRotation(dic);
            }
            else
            {
                _animator.SetFloat(VelocityXHash, horizontal, animDampTime, Time.deltaTime);
                _animator.SetFloat(VelocityZHash, vertical, animDampTime, Time.deltaTime);
            }

            //_animator.SetBool("IsWalking", isMoving);

        }

    }
}

// if (isMoving)
// {
//     Vector3 dic = raw.normalized;
//     _controller.Move(dic * moveSpeed * Time.deltaTime);

//     //transform.rotation = Quaternion.LookRotation(dic);
// }

// //_animator.SetBool("IsWalking", isMoving);
// _animator.SetFloat(VelocityXHash, horizontal, animDampTime, Time.deltaTime);
// _animator.SetFloat(VelocityZHash, vertical, animDampTime, Time.deltaTime);