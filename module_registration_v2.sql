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
-- Database: `module_registration_v2`
--

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
(25, 'Can add Contact Message', 7, 'add_contactmessage'),
(26, 'Can change Contact Message', 7, 'change_contactmessage'),
(27, 'Can delete Contact Message', 7, 'delete_contactmessage'),
(28, 'Can view Contact Message', 7, 'view_contactmessage'),
(29, 'Can add OTP Verification', 8, 'add_otpverification'),
(30, 'Can change OTP Verification', 8, 'change_otpverification'),
(31, 'Can delete OTP Verification', 8, 'delete_otpverification'),
(32, 'Can view OTP Verification', 8, 'view_otpverification'),
(33, 'Can add Student', 9, 'add_student'),
(34, 'Can change Student', 9, 'change_student'),
(35, 'Can delete Student', 9, 'delete_student'),
(36, 'Can view Student', 9, 'view_student'),
(37, 'Can add Module', 10, 'add_module'),
(38, 'Can change Module', 10, 'change_module'),
(39, 'Can delete Module', 10, 'delete_module'),
(40, 'Can view Module', 10, 'view_module'),
(41, 'Can add Registration', 11, 'add_registration'),
(42, 'Can change Registration', 11, 'change_registration'),
(43, 'Can delete Registration', 11, 'delete_registration'),
(44, 'Can view Registration', 11, 'view_registration'),
(45, 'Can add News Update', 12, 'add_newsupdate'),
(46, 'Can change News Update', 12, 'change_newsupdate'),
(47, 'Can delete News Update', 12, 'delete_newsupdate'),
(48, 'Can view News Update', 12, 'view_newsupdate'),
(49, 'Can add Site Configuration', 13, 'add_siteconfiguration'),
(50, 'Can change Site Configuration', 13, 'change_siteconfiguration'),
(51, 'Can delete Site Configuration', 13, 'delete_siteconfiguration'),
(52, 'Can view Site Configuration', 13, 'view_siteconfiguration');

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
(1, 'pbkdf2_sha256$1000000$hieVFsLDjhBb1hr2eXDS4n$iLmuvFNaWvMFqCxLbJs2TjdJ3WRki3QeNRJAzyvyexQ=', '2025-08-02 07:30:05.158020', 0, 'john_doe', 'John', 'Doe', 'john.doe@student.university.edu', 0, 1, '2025-07-31 08:28:08.411141'),
(2, 'pbkdf2_sha256$1000000$azaJqqCrZLlimQIGJk0nNK$8JCTddc4lydFsL41hTUlk0m7uKUn08CS4dgIr8xnj3U=', NULL, 0, 'jane_smith', 'Jane', 'Smith', 'jane.smith@student.university.edu', 0, 1, '2025-07-31 08:28:08.971907'),
(3, 'pbkdf2_sha256$1000000$7JwUNxELrp64ZbfvGpQICn$oPebhSX11VzbIml/6lUoQ9XOLfua98PfBaoY3ko8qdg=', NULL, 0, 'mike_johnson', 'Mike', 'Johnson', 'mike.johnson@student.university.edu', 0, 1, '2025-07-31 08:28:09.480537'),
(4, 'pbkdf2_sha256$1000000$h8BNjOR5CZyJaIUH0dFX68$hf4xFEnh4yWIZsxjYsJLpRgR7wPjl5FGQcn/bUva9Yw=', NULL, 0, 'sarah_wilson', 'Sarah', 'Wilson', 'sarah.wilson@student.university.edu', 0, 1, '2025-07-31 08:28:09.974737'),
(5, 'pbkdf2_sha256$1000000$j98X7RUQwCtXvXL5EnCG5O$8V7pcx0qfHpYNow5Y3jJ1TRF8+2z7X+Vruq9qvQH7Y0=', '2025-08-02 07:23:40.800547', 0, 'lakshmanan_kumar1', 'Lakshmanan', 'R', 'lakshmanan.coder@gmail.com', 0, 1, '2025-07-31 19:40:32.777391'),
(6, 'pbkdf2_sha256$1000000$DyPdavxbQ6LVGgzkPD589Y$i/RCeN7CFLRlcYW89B6Qi2UBIqEbHqmAFE6L4Mnirag=', '2025-07-31 19:52:33.881791', 1, 'admin1', '', '', 'admin@gmail.com', 1, 1, '2025-07-31 19:52:20.478944'),
(7, 'pbkdf2_sha256$1000000$ViDMfWXK12h4rbjbkquY9s$mXE5TQu6Yp5jj5h4T9jZC7Cqo14JYt1srCeMsMXui9A=', NULL, 0, 'lakshmanan_kumar2', 'Test', 'TEst', 'lakshmanan.w3dev@gmail.com', 0, 0, '2025-07-31 20:22:33.371716'),
(8, 'pbkdf2_sha256$1000000$RFWyfC059kzRHEKHG5CrjM$muWHrw5JrUHve2AG0jcmxQfbEwfTmD07kyZ1Gs2DAHM=', NULL, 0, 'chinnamaruthu', 'chinnamaruthu', 'designer', 'chinnamaruthu.designer@gmail.com', 0, 0, '2025-08-02 07:24:26.812924'),
(9, 'pbkdf2_sha256$1000000$aVbZI5ivNa6SGJqPdb6KXq$J8V5LQ9IBYYynOeaQPG8kTnraOzmXx1e/v4wda9LVfM=', '2025-08-02 09:41:46.995925', 0, 'klakshmanan48', 'klakshmanan', '48', 'klakshmanan48@gmail.com', 0, 1, '2025-08-02 09:00:11.610450');

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
-- Table structure for table `contact_messages`
--

CREATE TABLE `contact_messages` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `phone` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `contact_messages`
--

INSERT INTO `contact_messages` (`id`, `name`, `email`, `subject`, `message`, `created_at`, `is_read`, `phone`) VALUES
(1, 'Alex Thompson', 'alex.thompson@email.com', 'Question about module prerequisites', 'I would like to know more about the prerequisites for the Advanced Database Systems module. Could you please provide more information?', '2025-07-31 08:28:10.594364', 0, NULL),
(2, 'Emily Chen', 'emily.chen@email.com', 'Registration deadline inquiry', 'What is the deadline for module registration for the current semester? I want to make sure I don\'t miss it.', '2025-07-31 08:28:10.595657', 1, NULL),
(3, 'David Rodriguez', 'david.rodriguez@email.com', 'Technical support needed', 'I am having trouble accessing my student dashboard. Could someone help me resolve this issue?', '2025-07-31 08:28:10.595657', 0, NULL),
(4, 'asdf', 'asdf@asdf.asdf', 'General Inquiry', 'asdf', '2025-07-31 20:21:52.194433', 0, NULL);

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
(7, 'accounts', 'contactmessage'),
(8, 'accounts', 'otpverification'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(10, 'modules', 'module'),
(12, 'portalcontent', 'newsupdate'),
(13, 'portalcontent', 'siteconfiguration'),
(11, 'registrations', 'registration'),
(6, 'sessions', 'session'),
(9, 'students', 'student');

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
(1, 'contenttypes', '0001_initial', '2025-07-31 08:27:55.903594'),
(2, 'auth', '0001_initial', '2025-07-31 08:27:56.140729'),
(3, 'accounts', '0001_initial', '2025-07-31 08:27:56.176669'),
(4, 'accounts', '0002_contactmessage_phone', '2025-07-31 08:27:56.181690'),
(5, 'admin', '0001_initial', '2025-07-31 08:27:56.269078'),
(6, 'admin', '0002_logentry_remove_auto_add', '2025-07-31 08:27:56.284069'),
(7, 'admin', '0003_logentry_add_action_flag_choices', '2025-07-31 08:27:56.289812'),
(8, 'contenttypes', '0002_remove_content_type_name', '2025-07-31 08:27:56.322259'),
(9, 'auth', '0002_alter_permission_name_max_length', '2025-07-31 08:27:56.353856'),
(10, 'auth', '0003_alter_user_email_max_length', '2025-07-31 08:27:56.366212'),
(11, 'auth', '0004_alter_user_username_opts', '2025-07-31 08:27:56.372688'),
(12, 'auth', '0005_alter_user_last_login_null', '2025-07-31 08:27:56.392968'),
(13, 'auth', '0006_require_contenttypes_0002', '2025-07-31 08:27:56.394353'),
(14, 'auth', '0007_alter_validators_add_error_messages', '2025-07-31 08:27:56.394353'),
(15, 'auth', '0008_alter_user_username_max_length', '2025-07-31 08:27:56.410575'),
(16, 'auth', '0009_alter_user_last_name_max_length', '2025-07-31 08:27:56.421250'),
(17, 'auth', '0010_alter_group_name_max_length', '2025-07-31 08:27:56.430578'),
(18, 'auth', '0011_update_proxy_permissions', '2025-07-31 08:27:56.440782'),
(19, 'auth', '0012_alter_user_first_name_max_length', '2025-07-31 08:27:56.451528'),
(20, 'modules', '0001_initial', '2025-07-31 08:27:56.540470'),
(21, 'modules', '0002_module_image_url_alter_module_description', '2025-07-31 08:27:56.553881'),
(22, 'modules', '0003_module_max_students', '2025-07-31 08:27:56.559556'),
(23, 'portalcontent', '0001_initial', '2025-07-31 08:27:56.587699'),
(24, 'students', '0001_initial', '2025-07-31 08:27:56.628245'),
(25, 'registrations', '0001_initial', '2025-07-31 08:27:56.719640'),
(26, 'sessions', '0001_initial', '2025-07-31 08:27:56.743254'),
(27, 'modules', '0004_remove_module_semester', '2025-07-31 08:48:39.768625'),
(28, 'portalcontent', '0002_siteconfiguration_is_registration_open', '2025-07-31 20:09:25.767073');

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
('d3hcjltklkulq0jbacb6g6uerj6yrvjc', '.eJxVjDsOwjAQBe_iGlnJ-k9JnzNYXq-NA8iW4qRC3J1ESgHtm5n3Zj5sa_FbT4ufiV2ZYpffDUN8pnoAeoR6bzy2ui4z8kPhJ-18apRet9P9Oyihl72OOqHTWhuHloQhIxRkcGmwyjmQKkMUMCJaKaNNAGoPKERSgnDMbmCfL9QYN78:1uhZrK:X1rko7HDN9vAGauApv5XbQrQ5pXmbNbRVgPgQHyj0Uo', '2025-07-31 21:26:38.695318'),
('s32yoeeblzdqbire3g0l97xr3hzjvvjl', '.eJxVjLsOAiEUBf-F2hDeD0v7_QbChYusGkiW3cr474ZkC23PzJw3CfHYazgGbmHN5Eo8ufxuENMT2wT5Edu909Tbvq1Ap0JPOujSM75up_t3UOOos7bMWRSea62dLKwAaikckwq8QBDcipQhm8KsSR6Ud8gyVyJ6k6ZGPl_Kmjcf:1ui8kN:bzC2hWJH6GFVbKdC6mVx3h5MB4_fmxJHcfCKfQWJJro', '2025-08-02 10:41:47.001235');

-- --------------------------------------------------------

--
-- Table structure for table `modules`
--

CREATE TABLE `modules` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `code` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `credits` int(10) UNSIGNED NOT NULL CHECK (`credits` >= 0),
  `category` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `image_url` varchar(500) DEFAULT NULL,
  `max_students` int(10) UNSIGNED NOT NULL CHECK (`max_students` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `modules`
--

INSERT INTO `modules` (`id`, `name`, `code`, `description`, `credits`, `category`, `is_active`, `created_at`, `updated_at`, `image_url`, `max_students`) VALUES
(1, 'Introduction to Computer Science', 'CS101', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 3, 'CORE', 1, '2025-07-31 08:28:08.374457', '2025-07-31 08:28:08.374457', 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80', 50),
(2, 'Data Structures and Algorithms', 'CS201', 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 4, 'CORE', 1, '2025-07-31 08:28:08.384996', '2025-07-31 08:28:08.384996', 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80', 50),
(3, 'Database Systems', 'CS301', 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 3, 'SPECIALIZED', 1, '2025-07-31 08:28:08.384996', '2025-07-31 08:28:08.384996', 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80', 50),
(4, 'Calculus I', 'MATH101', 'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 4, 'CORE', 1, '2025-07-31 08:28:08.384996', '2025-07-31 08:28:08.384996', 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80', 50),
(5, 'Linear Algebra', 'MATH201', 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.', 3, 'CORE', 1, '2025-07-31 08:28:08.384996', '2025-07-31 08:28:08.384996', 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80', 50),
(6, 'Academic Writing', 'ENG101', 'Totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt.', 3, 'CORE', 1, '2025-07-31 08:28:08.399760', '2025-07-31 08:28:08.399760', 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80', 50),
(7, 'Physics I', 'PHYS101', 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.', 4, 'ELECTIVE', 1, '2025-07-31 08:28:08.399760', '2025-07-31 08:28:08.399760', 'https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80', 50),
(8, 'Machine Learning', 'CS401', 'Sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.', 3, 'SPECIALIZED', 1, '2025-07-31 08:28:08.399760', '2025-07-31 08:28:08.399760', 'https://images.unsplash.com/photo-1677442136019-21780ecad995?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80', 50),
(9, 'Test', 'TST101', 'Test', 3, 'CORE', 1, '2025-07-31 09:30:55.059341', '2025-07-31 09:30:55.059341', NULL, 50);

-- --------------------------------------------------------

--
-- Table structure for table `modules_prerequisites`
--

CREATE TABLE `modules_prerequisites` (
  `id` bigint(20) NOT NULL,
  `from_module_id` bigint(20) NOT NULL,
  `to_module_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `news_updates`
--

CREATE TABLE `news_updates` (
  `id` bigint(20) NOT NULL,
  `title` varchar(200) NOT NULL,
  `slug` varchar(255) DEFAULT NULL,
  `content` longtext NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `news_updates`
--

INSERT INTO `news_updates` (`id`, `title`, `slug`, `content`, `is_published`, `created_at`, `updated_at`) VALUES
(1, 'Welcome to Fall 2024 Semester', 'welcome-to-fall-2024-semester', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.', 1, '2025-07-31 08:28:10.564866', '2025-07-31 08:28:10.564866'),
(2, 'New Computer Science Modules Added', 'new-computer-science-modules-added', 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim.', 1, '2025-07-31 08:28:10.564866', '2025-07-31 08:28:10.564866'),
(3, 'Campus Library Extended Hours', 'campus-library-extended-hours', 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis.', 1, '2025-07-31 08:28:10.578686', '2025-07-31 08:28:10.578686'),
(4, 'Spring 2025 Registration Opens Soon', 'spring-2025-registration-opens-soon', 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.', 0, '2025-07-31 08:28:10.578686', '2025-07-31 08:28:10.578686');

-- --------------------------------------------------------

--
-- Table structure for table `otp_verifications`
--

CREATE TABLE `otp_verifications` (
  `id` bigint(20) NOT NULL,
  `otp_code` varchar(6) NOT NULL,
  `otp_type` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `otp_verifications`
--

INSERT INTO `otp_verifications` (`id`, `otp_code`, `otp_type`, `created_at`, `expires_at`, `is_used`, `user_id`) VALUES
(2, '535111', '', '2025-07-31 19:46:26.994133', '2025-07-31 20:01:26.994133', 1, 5),
(4, '937364', '', '2025-07-31 20:23:00.304544', '2025-07-31 20:38:00.304544', 0, 7),
(5, '077708', '', '2025-08-02 07:24:27.510092', '2025-08-02 07:39:27.510092', 0, 8),
(6, '077770', 'REGISTER', '2025-08-02 09:00:12.237200', '2025-08-02 09:15:12.237200', 1, 9);

-- --------------------------------------------------------

--
-- Table structure for table `registrations`
--

CREATE TABLE `registrations` (
  `id` bigint(20) NOT NULL,
  `registration_date` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `grade` varchar(2) NOT NULL,
  `notes` longtext NOT NULL,
  `module_id` bigint(20) NOT NULL,
  `student_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `registrations`
--

INSERT INTO `registrations` (`id`, `registration_date`, `status`, `grade`, `notes`, `module_id`, `student_id`) VALUES
(1, '2025-07-31 08:28:10.474334', 'completed', '', '', 3, 1),
(2, '2025-07-31 08:28:10.483292', 'completed', '', '', 4, 1),
(3, '2025-07-31 08:28:10.483292', 'pending', '', '', 8, 1),
(4, '2025-07-31 08:28:10.483292', 'enrolled', 'D', '', 7, 2),
(5, '2025-07-31 08:28:10.483292', 'enrolled', '', '', 5, 2),
(6, '2025-07-31 08:28:10.501083', 'enrolled', '', '', 3, 2),
(7, '2025-07-31 08:28:10.507389', 'pending', '', '', 6, 2),
(8, '2025-07-31 08:28:10.507389', 'enrolled', 'B', '', 6, 3),
(9, '2025-07-31 08:28:10.519186', 'completed', '', '', 4, 3),
(10, '2025-07-31 08:28:10.525629', 'completed', 'D', '', 8, 3),
(11, '2025-07-31 08:28:10.531018', 'pending', '', '', 2, 4),
(12, '2025-07-31 08:28:10.531018', 'completed', '', '', 4, 4),
(13, '2025-07-31 08:28:10.531018', 'completed', '', '', 6, 4),
(14, '2025-07-31 08:28:10.546984', 'enrolled', 'D', '', 7, 4),
(15, '2025-07-31 17:43:15.448189', 'pending', '', '', 7, 1),
(16, '2025-07-31 17:43:15.451016', 'pending', '', '', 5, 1),
(17, '2025-07-31 17:43:15.451016', 'completed', '', '', 2, 2),
(18, '2025-07-31 17:43:15.460467', 'pending', 'D', '', 1, 2),
(19, '2025-07-31 17:43:15.463630', 'completed', 'B', '', 1, 3),
(20, '2025-07-31 17:43:15.465698', 'enrolled', '', '', 9, 4),
(21, '2025-07-31 17:43:15.465698', 'completed', '', '', 5, 4),
(22, '2025-07-31 17:43:15.465698', 'completed', 'C', '', 8, 4),
(23, '2025-07-31 17:44:12.447477', 'enrolled', 'D', '', 9, 1),
(24, '2025-07-31 17:44:12.460383', 'pending', '', '', 7, 3),
(25, '2025-07-31 17:44:12.467272', 'pending', '', '', 1, 4),
(26, '2025-07-31 20:10:31.218061', 'pending', '', '', 2, 5),
(27, '2025-07-31 20:19:38.128891', 'pending', '', '', 1, 5),
(28, '2025-08-02 07:30:21.510271', 'pending', '', '', 2, 1),
(29, '2025-08-02 09:02:38.917333', 'pending', '', '', 1, 6);

-- --------------------------------------------------------

--
-- Table structure for table `site_configuration`
--

CREATE TABLE `site_configuration` (
  `id` bigint(20) NOT NULL,
  `site_name` varchar(100) NOT NULL,
  `site_description` longtext NOT NULL,
  `contact_email` varchar(254) NOT NULL,
  `contact_phone` varchar(20) NOT NULL,
  `address` longtext NOT NULL,
  `about_content` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_registration_open` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `site_configuration`
--

INSERT INTO `site_configuration` (`id`, `site_name`, `site_description`, `contact_email`, `contact_phone`, `address`, `about_content`, `is_active`, `created_at`, `updated_at`, `is_registration_open`) VALUES
(1, 'University Module Registration System', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 'info@university.edu', '+1-555-123-4567', '123 University Ave, Academic City, State 12345', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 1, '2025-07-31 08:28:08.374457', '2025-07-31 08:28:08.374457', 1);

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` bigint(20) NOT NULL,
  `student_id` varchar(20) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `phone_number` varchar(15) NOT NULL,
  `address` varchar(255) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `student_id`, `date_of_birth`, `phone_number`, `address`, `profile_picture`, `created_at`, `user_id`) VALUES
(1, 'STU00001', NULL, '+1-555-001-0001', '123 Student St, Campus City, State 12345', '', '2025-07-31 08:28:08.962569', 1),
(2, 'STU00002', NULL, '+1-555-001-0002', '456 University Ave, Campus City, State 12345', '', '2025-07-31 08:28:09.478775', 2),
(3, 'STU00003', NULL, '+1-555-001-0003', '789 Academic Blvd, Campus City, State 12345', '', '2025-07-31 08:28:09.974737', 3),
(4, 'STU00004', NULL, '+1-555-001-0004', '321 Scholar Lane, Campus City, State 12345', '', '2025-07-31 08:28:10.467582', 4),
(5, 'Lakshmanan r', '2025-08-06', '6382775774', 'asdf', 'student_profiles/IMG20250730142404.jpg', '2025-07-31 19:47:08.690635', 5),
(6, 'STU12345', '2025-08-07', '6382775774', 'test, test, test', 'student_profiles/e6da3959adbb9acf4ea5625571e508a3_RrRS4vH.jpg', '2025-08-02 09:00:59.096454', 9);

--
-- Indexes for dumped tables
--

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
-- Indexes for table `contact_messages`
--
ALTER TABLE `contact_messages`
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
-- Indexes for table `modules`
--
ALTER TABLE `modules`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`);

--
-- Indexes for table `modules_prerequisites`
--
ALTER TABLE `modules_prerequisites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `modules_prerequisites_from_module_id_to_module_id_618ce52c_uniq` (`from_module_id`,`to_module_id`),
  ADD KEY `modules_prerequisites_to_module_id_33b9f7f4_fk_modules_id` (`to_module_id`);

--
-- Indexes for table `news_updates`
--
ALTER TABLE `news_updates`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexes for table `otp_verifications`
--
ALTER TABLE `otp_verifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `otp_verifications_user_id_3340c576_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `registrations`
--
ALTER TABLE `registrations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `registrations_student_id_module_id_00973d1a_uniq` (`student_id`,`module_id`),
  ADD KEY `registrations_module_id_973291df_fk_modules_id` (`module_id`);

--
-- Indexes for table `site_configuration`
--
ALTER TABLE `site_configuration`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `student_id` (`student_id`),
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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

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
-- AUTO_INCREMENT for table `contact_messages`
--
ALTER TABLE `contact_messages`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `modules`
--
ALTER TABLE `modules`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `modules_prerequisites`
--
ALTER TABLE `modules_prerequisites`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `news_updates`
--
ALTER TABLE `news_updates`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `otp_verifications`
--
ALTER TABLE `otp_verifications`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `registrations`
--
ALTER TABLE `registrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `site_configuration`
--
ALTER TABLE `site_configuration`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

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
-- Constraints for table `modules_prerequisites`
--
ALTER TABLE `modules_prerequisites`
  ADD CONSTRAINT `modules_prerequisites_from_module_id_8549358d_fk_modules_id` FOREIGN KEY (`from_module_id`) REFERENCES `modules` (`id`),
  ADD CONSTRAINT `modules_prerequisites_to_module_id_33b9f7f4_fk_modules_id` FOREIGN KEY (`to_module_id`) REFERENCES `modules` (`id`);

--
-- Constraints for table `otp_verifications`
--
ALTER TABLE `otp_verifications`
  ADD CONSTRAINT `otp_verifications_user_id_3340c576_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `registrations`
--
ALTER TABLE `registrations`
  ADD CONSTRAINT `registrations_module_id_973291df_fk_modules_id` FOREIGN KEY (`module_id`) REFERENCES `modules` (`id`),
  ADD CONSTRAINT `registrations_student_id_f73ba554_fk_students_id` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`);

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_user_id_42864fc9_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
