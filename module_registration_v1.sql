-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 02, 2025 at 12:04 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `module_registration_v1`
--

-- --------------------------------------------------------

--
-- Table structure for table `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Token', 7, 'add_token'),
(26, 'Can change Token', 7, 'change_token'),
(27, 'Can delete Token', 7, 'delete_token'),
(28, 'Can view Token', 7, 'view_token'),
(29, 'Can add Token', 8, 'add_tokenproxy'),
(30, 'Can change Token', 8, 'change_tokenproxy'),
(31, 'Can delete Token', 8, 'delete_tokenproxy'),
(32, 'Can view Token', 8, 'view_tokenproxy'),
(33, 'Can add contact', 9, 'add_contact'),
(34, 'Can change contact', 9, 'change_contact'),
(35, 'Can delete contact', 9, 'delete_contact'),
(36, 'Can view contact', 9, 'view_contact'),
(37, 'Can add email verification', 10, 'add_emailverification'),
(38, 'Can change email verification', 10, 'change_emailverification'),
(39, 'Can delete email verification', 10, 'delete_emailverification'),
(40, 'Can view email verification', 10, 'view_emailverification'),
(41, 'Can add password reset otp', 11, 'add_passwordresetotp'),
(42, 'Can change password reset otp', 11, 'change_passwordresetotp'),
(43, 'Can delete password reset otp', 11, 'delete_passwordresetotp'),
(44, 'Can view password reset otp', 11, 'view_passwordresetotp'),
(45, 'Can add student', 12, 'add_student'),
(46, 'Can change student', 12, 'change_student'),
(47, 'Can delete student', 12, 'delete_student'),
(48, 'Can view student', 12, 'view_student'),
(49, 'Can add module', 13, 'add_module'),
(50, 'Can change module', 13, 'change_module'),
(51, 'Can delete module', 13, 'delete_module'),
(52, 'Can view module', 13, 'view_module'),
(53, 'Can add registration', 14, 'add_registration'),
(54, 'Can change registration', 14, 'change_registration'),
(55, 'Can delete registration', 14, 'delete_registration'),
(56, 'Can view registration', 14, 'view_registration');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$UfuKu3fDTv8KjWg5DEuzxg$VK6iJI4XDE8YJAd1XBRC2z6D5lizPZM2aNbin9c6ZQ0=', '2025-07-30 20:25:12.627833', 1, 'admin', '', '', 'admin@example.com', 1, 1, '2025-07-30 20:21:38.403840'),
(2, 'pbkdf2_sha256$1000000$0NFFK1S2C0Npxtwoko3zfP$mYzaC68/sU42rGR/7eqGqBoBcA7Icx6HjIBkVMSiOTo=', NULL, 0, 'john_doe', 'John', 'Doe', 'john.doe@student.university.edu', 0, 1, '2025-07-30 20:21:51.330850'),
(3, 'pbkdf2_sha256$1000000$4bgu9OL1yWG4ly2rCb2S0e$yTvfZkCPKGYhi4QYYdJqGvvW4HROO+K9/t5z7uum7no=', NULL, 0, 'jane_smith', 'Jane', 'Smith', 'jane.smith@student.university.edu', 0, 1, '2025-07-30 20:21:51.767959'),
(4, 'pbkdf2_sha256$1000000$Jqp0bakIMA9k1U2g9VIXBO$ywQpizRldloaaVh9xZKAeH/5OIaWXx6FR9AIpjS/8Cw=', NULL, 0, 'bob_wilson', 'Bob', 'Wilson', 'bob.wilson@student.university.edu', 0, 1, '2025-07-30 20:21:52.219742'),
(5, 'pbkdf2_sha256$1000000$QpmIerVnirk6ciZYXV7BLE$hOPbsRRNcVOlW2RTzC7gEqEPUFeot3VTNyBLWvhYJOw=', NULL, 0, 'alice_brown', 'Alice', 'Brown', 'alice.brown@student.university.edu', 0, 1, '2025-07-30 20:21:52.654508'),
(6, 'pbkdf2_sha256$1000000$mkZOcoTE42DH6yTfE7HQXG$6EAL9WZZ1lrUKn7IaPGgnWpTlds4KKoEGrCohzebgdM=', NULL, 0, 'charlie_davis', 'Charlie', 'Davis', 'charlie.davis@student.university.edu', 0, 1, '2025-07-30 20:21:53.101439'),
(7, 'pbkdf2_sha256$1000000$Wis5xHy0dtRmAKukfCEWHw$y9P4PO++K4y5LTl6HGRIMgHFJYXjqRMiEc7DHOfNiu4=', '2025-08-02 07:19:57.896452', 0, 'lakshmanan_kumar1', 'Lakshmanan', 'R', 'lakshmanan.coder@gmail.com', 0, 1, '2025-07-31 19:42:27.156514'),
(8, 'pbkdf2_sha256$1000000$uqylgQm1fI1VuzcU6jcaxZ$23DMt0cJ4/x0D4fdV+Q/JylfkbN2X2sK5tepPcgWq/U=', '2025-08-02 08:45:11.458090', 0, 'klakshmanan48', 'klakshmanan48@gmail.com', 'klakshmanan48@gmail.com', 'klakshmanan48@gmail.com', 0, 1, '2025-08-02 08:42:16.449535');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_contact`
--

CREATE TABLE `core_contact` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `core_contact`
--

INSERT INTO `core_contact` (`id`, `name`, `email`, `subject`, `message`, `created_at`) VALUES
(1, 'asdfa', 'sdfasd@asdf.asdf', 'asdf', 'asdf', '2025-07-30 20:25:33.678356');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(7, 'authtoken', 'token'),
(8, 'authtoken', 'tokenproxy'),
(5, 'contenttypes', 'contenttype'),
(9, 'core', 'contact'),
(13, 'modules', 'module'),
(14, 'modules', 'registration'),
(6, 'sessions', 'session'),
(10, 'students', 'emailverification'),
(11, 'students', 'passwordresetotp'),
(12, 'students', 'student');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-07-30 20:21:06.046325'),
(2, 'auth', '0001_initial', '2025-07-30 20:21:06.252822'),
(3, 'admin', '0001_initial', '2025-07-30 20:21:06.299443'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-07-30 20:21:06.307342'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-07-30 20:21:06.311947'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-07-30 20:21:06.336895'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-07-30 20:21:06.351923'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-07-30 20:21:06.363587'),
(9, 'auth', '0004_alter_user_username_opts', '2025-07-30 20:21:06.367374'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-07-30 20:21:06.382890'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-07-30 20:21:06.382890'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-07-30 20:21:06.393628'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-07-30 20:21:06.400560'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-07-30 20:21:06.410866'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-07-30 20:21:06.416620'),
(16, 'auth', '0011_update_proxy_permissions', '2025-07-30 20:21:06.427100'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-07-30 20:21:06.433822'),
(18, 'authtoken', '0001_initial', '2025-07-30 20:21:06.460970'),
(19, 'authtoken', '0002_auto_20160226_1747', '2025-07-30 20:21:06.476689'),
(20, 'authtoken', '0003_tokenproxy', '2025-07-30 20:21:06.483437'),
(21, 'authtoken', '0004_alter_tokenproxy_options', '2025-07-30 20:21:06.483437'),
(22, 'core', '0001_initial', '2025-07-30 20:21:06.493729'),
(23, 'students', '0001_initial', '2025-07-30 20:21:06.584477'),
(24, 'modules', '0001_initial', '2025-07-30 20:21:06.649365'),
(25, 'sessions', '0001_initial', '2025-07-30 20:21:06.664658');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('nfvroorf0j6ohzv5mtef44upnuchbpp0', '.eJxVjMsOwiAUBf-FtSE8SgCX7v0Gch8gVUOT0q4a_92QdKHbMzPnEAn2raa95zXNLK4iiMvvhkCv3AbgJ7THImlp2zqjHIo8aZf3hfP7drp_BxV6HbVT7EwwVIzyKiLbqH1ECsGSQY-TzxoDUrbFOYd2AiDrFBitALhY8fkC4UE4Hg:1ui7rb:ikx_nhfvnouzPdj0iYNY8hu5Wz_JagvNt4i-Qm32CCI', '2025-08-16 08:45:11.460450'),
('tk3epawyg9p03a2oed5rm0bf096vi5uo', '.eJxVjDsOwjAQBe_iGlmOg72Gkj5nsPYXHECJFCcV4u7IUgpo38y8t8m4byXvVdc8ibkaMKffjZCfOjcgD5zvi-Vl3taJbFPsQasdFtHX7XD_DgrW0mqnHGDUDmgMpD16BO1DCnKBlHyA6JJIHzH6jh0zRRIFFxmRz0hqPl8AkTjy:1uhZAt:k5YXLN4IG5qPn9HXmrnk7utmAy7-mMLMB12eqtxAH9Q', '2025-08-14 19:42:47.972018'),
('yklrbz937w2t38ljoidb6ohunhipcv0q', '.eJxVjDsOwjAQBe_iGlmOg72Gkj5nsPYXHECJFCcV4u7IUgpo38y8t8m4byXvVdc8ibkaMKffjZCfOjcgD5zvi-Vl3taJbFPsQasdFtHX7XD_DgrW0mqnHGDUDmgMpD16BO1DCnKBlHyA6JJIHzH6jh0zRRIFFxmRz0hqPl8AkTjy:1ui6X7:6GLcZHJaZ-hq5oFdg6PtagwdiVTIjxGS3CA9lCFf6PY', '2025-08-16 07:19:57.896452'),
('z1k55061h7zs9mab2wao6o3xws9yg90d', '.eJxVjDsOwjAQBe_iGlnrTxSbkp4zROv1Lg4gW8qnirg7iZQC2pl5b1MDrksZ1pmnYczqqoy6_LKE9OJ6iPzE-miaWl2mMekj0aed9b1lft_O9u-g4Fz2tVgIIUjIsfNARD1bYxmAAu4QMYhH6LwYY6PrIXEHIsaRswKWfVSfL-SrN8c:1uhDMO:dOBTTeenykCWfcl4r0vs8yJu0xm1GDq8XUzK7tS3mw8', '2025-08-13 20:25:12.631072');

-- --------------------------------------------------------

--
-- Table structure for table `modules_module`
--

CREATE TABLE `modules_module` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `code` varchar(20) NOT NULL,
  `credit` int(10) UNSIGNED NOT NULL CHECK (`credit` >= 0),
  `category` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `availability` tinyint(1) NOT NULL,
  `max_students` int(10) UNSIGNED NOT NULL CHECK (`max_students` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `modules_module`
--

INSERT INTO `modules_module` (`id`, `name`, `code`, `credit`, `category`, `description`, `availability`, `max_students`, `created_at`, `updated_at`) VALUES
(1, 'Introduction to Computer Science', 'CS101', 3, 'core', 'Fundamental concepts of computer science including programming basics, algorithms, and data structures.', 1, 30, '2025-07-30 20:21:51.297639', '2025-07-30 20:21:51.297639'),
(2, 'Database Management Systems', 'CS201', 4, 'core', 'Comprehensive study of database design, SQL, normalization, and database administration.', 1, 25, '2025-07-30 20:21:51.302009', '2025-07-30 20:21:51.303020'),
(3, 'Web Development', 'CS301', 3, 'elective', 'Modern web development techniques using HTML, CSS, JavaScript, and popular frameworks.', 1, 20, '2025-07-30 20:21:51.305253', '2025-07-30 20:21:51.305253'),
(4, 'Data Analytics', 'DA101', 3, 'elective', 'Introduction to data analysis, statistical methods, and data visualization techniques.', 1, 25, '2025-07-30 20:21:51.305253', '2025-07-30 20:21:51.305253'),
(5, 'Machine Learning', 'ML201', 4, 'elective', 'Fundamentals of machine learning algorithms, supervised and unsupervised learning.', 1, 20, '2025-07-30 20:21:51.313082', '2025-07-30 20:21:51.313082'),
(6, 'Software Engineering', 'SE301', 3, 'core', 'Software development lifecycle, design patterns, testing, and project management.', 1, 30, '2025-07-30 20:21:51.316779', '2025-07-30 20:21:51.316779'),
(7, 'Mobile App Development', 'MAD201', 3, 'elective', 'Development of mobile applications for iOS and Android platforms.', 1, 15, '2025-07-30 20:21:51.320492', '2025-07-30 20:21:51.320492'),
(8, 'Cybersecurity Fundamentals', 'CYB101', 3, 'optional', 'Introduction to cybersecurity concepts, threats, and protection mechanisms.', 1, 25, '2025-07-30 20:21:51.323054', '2025-07-30 20:21:51.323054'),
(9, 'Digital Marketing', 'MKT201', 2, 'optional', 'Digital marketing strategies, social media marketing, and online advertising.', 1, 30, '2025-07-30 20:21:51.325809', '2025-07-30 20:21:51.325809'),
(10, 'Project Management', 'PM101', 2, 'optional', 'Project planning, execution, monitoring, and risk management principles.', 1, 35, '2025-07-30 20:21:51.328834', '2025-07-30 20:21:51.328834');

-- --------------------------------------------------------

--
-- Table structure for table `modules_registration`
--

CREATE TABLE `modules_registration` (
  `id` bigint(20) NOT NULL,
  `date_registered` datetime(6) NOT NULL,
  `module_id` bigint(20) NOT NULL,
  `student_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `modules_registration`
--

INSERT INTO `modules_registration` (`id`, `date_registered`, `module_id`, `student_id`) VALUES
(1, '2025-07-30 20:21:53.562095', 9, 4),
(2, '2025-07-30 20:21:53.566398', 8, 4),
(3, '2025-07-30 20:21:53.567724', 2, 4),
(4, '2025-07-30 20:21:53.567724', 5, 4),
(5, '2025-07-30 20:21:53.584459', 4, 3),
(6, '2025-07-30 20:21:53.587991', 1, 3),
(7, '2025-07-30 20:21:53.587991', 2, 3),
(8, '2025-07-30 20:21:53.599751', 4, 5),
(9, '2025-07-30 20:21:53.603934', 10, 5),
(10, '2025-07-30 20:21:53.603934', 6, 5),
(11, '2025-07-30 20:21:53.603934', 8, 5),
(12, '2025-07-30 20:21:53.616361', 10, 2),
(13, '2025-07-30 20:21:53.619362', 3, 2),
(14, '2025-07-30 20:21:53.623998', 4, 1),
(15, '2025-07-30 20:21:53.623998', 3, 1),
(17, '2025-08-02 10:02:40.951830', 7, 4),
(18, '2025-08-02 10:02:41.053909', 6, 4),
(19, '2025-08-02 10:02:41.060516', 6, 3),
(20, '2025-08-02 10:02:41.065546', 7, 3),
(21, '2025-08-02 10:02:41.072073', 9, 3),
(22, '2025-08-02 10:02:41.078217', 7, 5),
(23, '2025-08-02 10:02:41.089333', 1, 5),
(24, '2025-08-02 10:02:41.093697', 9, 2),
(25, '2025-08-02 10:02:41.095352', 5, 2),
(26, '2025-08-02 10:02:41.097350', 2, 2),
(27, '2025-08-02 10:02:41.097350', 10, 1),
(28, '2025-08-02 10:02:41.138959', 6, 1),
(29, '2025-08-02 10:02:41.141776', 1, 1),
(30, '2025-08-02 10:02:41.146709', 6, 7),
(31, '2025-08-02 10:02:41.146709', 8, 7),
(32, '2025-08-02 10:02:41.146709', 7, 7),
(33, '2025-08-02 10:02:41.153924', 3, 7),
(34, '2025-08-02 10:02:41.158105', 8, 6),
(35, '2025-08-02 10:02:41.160236', 9, 6),
(36, '2025-08-02 10:02:41.162228', 6, 6);

-- --------------------------------------------------------

--
-- Table structure for table `students_emailverification`
--

CREATE TABLE `students_emailverification` (
  `id` bigint(20) NOT NULL,
  `otp` varchar(6) NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `students_emailverification`
--

INSERT INTO `students_emailverification` (`id`, `otp`, `is_used`, `created_at`, `expires_at`, `user_id`) VALUES
(1, '321933', 1, '2025-07-31 19:42:27.893209', '2025-07-31 19:52:27.893209', 7),
(2, '552466', 1, '2025-08-02 08:42:17.289105', '2025-08-02 08:52:17.289105', 8);

-- --------------------------------------------------------

--
-- Table structure for table `students_passwordresetotp`
--

CREATE TABLE `students_passwordresetotp` (
  `id` bigint(20) NOT NULL,
  `otp` varchar(6) NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `students_passwordresetotp`
--

INSERT INTO `students_passwordresetotp` (`id`, `otp`, `is_used`, `created_at`, `expires_at`, `user_id`) VALUES
(1, '921313', 1, '2025-08-02 08:44:42.114731', '2025-08-02 08:54:42.114731', 8);

-- --------------------------------------------------------

--
-- Table structure for table `students_student`
--

CREATE TABLE `students_student` (
  `id` bigint(20) NOT NULL,
  `date_of_birth` date NOT NULL,
  `address` longtext NOT NULL,
  `city` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `is_email_verified` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `students_student`
--

INSERT INTO `students_student` (`id`, `date_of_birth`, `address`, `city`, `country`, `photo`, `is_email_verified`, `created_at`, `updated_at`, `user_id`) VALUES
(1, '2000-05-15', '123 Student Street', 'Boston', 'USA', '', 1, '2025-07-30 20:21:51.760904', '2025-07-30 20:21:51.760904', 2),
(2, '1999-08-22', '456 Campus Ave', 'Cambridge', 'USA', '', 1, '2025-07-30 20:21:52.219742', '2025-07-30 20:21:52.219742', 3),
(3, '2001-03-10', '789 University Blvd', 'New York', 'USA', '', 1, '2025-07-30 20:21:52.650917', '2025-07-30 20:21:52.650917', 4),
(4, '2000-11-05', '321 Education Lane', 'San Francisco', 'USA', '', 1, '2025-07-30 20:21:53.101439', '2025-07-30 20:21:53.101439', 5),
(5, '1998-12-18', '654 Learning St', 'Seattle', 'USA', '', 1, '2025-07-30 20:21:53.546384', '2025-07-30 20:21:53.546384', 6),
(6, '2025-08-07', 'test', 'chennai', 'India', 'student_photos/IMG_20250723_133527.jpg', 1, '2025-07-31 19:42:27.892263', '2025-08-02 07:20:20.951931', 7),
(7, '2025-07-29', 'klakshmanan48@gmail.com', 'klakshmanan48@gmail.com', 'klakshmanan48@gmail.com', '', 1, '2025-08-02 08:42:17.241096', '2025-08-02 08:42:33.971381', 8);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `core_contact`
--
ALTER TABLE `core_contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `modules_module`
--
ALTER TABLE `modules_module`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `modules_registration`
--
ALTER TABLE `modules_registration`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `modules_registration_student_id_module_id_5a2b0f58_uniq` (`student_id`,`module_id`),
  ADD KEY `modules_registration_module_id_3092449b_fk_modules_module_id` (`module_id`);

--
-- Indexes for table `students_emailverification`
--
ALTER TABLE `students_emailverification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `students_emailverification_user_id_4d8690d4_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `students_passwordresetotp`
--
ALTER TABLE `students_passwordresetotp`
  ADD PRIMARY KEY (`id`),
  ADD KEY `students_passwordresetotp_user_id_bfb659bc_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `students_student`
--
ALTER TABLE `students_student`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_contact`
--
ALTER TABLE `core_contact`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `modules_module`
--
ALTER TABLE `modules_module`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `modules_registration`
--
ALTER TABLE `modules_registration`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `students_emailverification`
--
ALTER TABLE `students_emailverification`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `students_passwordresetotp`
--
ALTER TABLE `students_passwordresetotp`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `students_student`
--
ALTER TABLE `students_student`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `modules_registration`
--
ALTER TABLE `modules_registration`
  ADD CONSTRAINT `modules_registration_module_id_3092449b_fk_modules_module_id` FOREIGN KEY (`module_id`) REFERENCES `modules_module` (`id`),
  ADD CONSTRAINT `modules_registration_student_id_9e0036f2_fk_students_student_id` FOREIGN KEY (`student_id`) REFERENCES `students_student` (`id`);

--
-- Constraints for table `students_emailverification`
--
ALTER TABLE `students_emailverification`
  ADD CONSTRAINT `students_emailverification_user_id_4d8690d4_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `students_passwordresetotp`
--
ALTER TABLE `students_passwordresetotp`
  ADD CONSTRAINT `students_passwordresetotp_user_id_bfb659bc_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `students_student`
--
ALTER TABLE `students_student`
  ADD CONSTRAINT `students_student_user_id_56286dbb_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
