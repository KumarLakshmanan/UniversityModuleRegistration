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
-- Database: `module_registration_v3`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(25, 'Can add OTP', 7, 'add_otp'),
(26, 'Can change OTP', 7, 'change_otp'),
(27, 'Can delete OTP', 7, 'delete_otp'),
(28, 'Can view OTP', 7, 'view_otp'),
(29, 'Can add Student', 8, 'add_student'),
(30, 'Can change Student', 8, 'change_student'),
(31, 'Can delete Student', 8, 'delete_student'),
(32, 'Can view Student', 8, 'view_student'),
(33, 'Can add Module', 9, 'add_module'),
(34, 'Can change Module', 9, 'change_module'),
(35, 'Can delete Module', 9, 'delete_module'),
(36, 'Can view Module', 9, 'view_module'),
(37, 'Can add Registration', 10, 'add_registration'),
(38, 'Can change Registration', 10, 'change_registration'),
(39, 'Can delete Registration', 10, 'delete_registration'),
(40, 'Can view Registration', 10, 'view_registration'),
(41, 'Can add Contact Message', 11, 'add_contactmessage'),
(42, 'Can change Contact Message', 11, 'change_contactmessage'),
(43, 'Can delete Contact Message', 11, 'delete_contactmessage'),
(44, 'Can view Contact Message', 11, 'view_contactmessage'),
(45, 'Can add System Statistics', 12, 'add_systemstats'),
(46, 'Can change System Statistics', 12, 'change_systemstats'),
(47, 'Can delete System Statistics', 12, 'delete_systemstats'),
(48, 'Can view System Statistics', 12, 'view_systemstats');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$NzhyyLA4h4fkGKDjrrs2na$gHETlq9AEv+cnwFUGjJKjDgPFi/CD0se+AeRpCGBixk=', '2025-07-31 19:05:25.231830', 1, 'admin', '', '', 'admin@example.com', 1, 1, '2025-07-31 17:50:49.701668'),
(2, 'pbkdf2_sha256$1000000$cqi6YhH1mruqScFGQiLFfW$UM3SoVVEvVY2H2psTEMqyBln+Nm/0xPQzlAfEtODqas=', '2025-07-31 19:24:20.656142', 0, 'john_doe', 'John', 'Doe', 'john@example.com', 0, 1, '2025-07-31 17:52:06.606103'),
(3, 'pbkdf2_sha256$1000000$Q9GzKKdAvNLeFGkIOYVlWA$CG+8Uk5vvHWjHsixWQ+77g6eNbFdeIVfp2/Hf2cewZo=', NULL, 0, 'jane_smith', 'Jane', 'Smith', 'jane@example.com', 0, 1, '2025-07-31 17:52:28.301113'),
(4, 'pbkdf2_sha256$1000000$bXjKIZWgVfsP3YFq9ole1c$vO43YqCi0XtILae+bFFEZmFdZH7bPe8Sx0Qx+M4imHg=', NULL, 0, 'mike_johnson', 'Mike', 'Johnson', 'mike@example.com', 0, 1, '2025-07-31 17:52:28.878732'),
(5, 'pbkdf2_sha256$1000000$j0YOR7UlbBOJkTbAXw57pY$hy0fDhMiyv3SBzhghapa89ns6iYwrdckRU9GbR0U64s=', NULL, 0, 'sarah_wilson', 'Sarah', 'Wilson', 'sarah@example.com', 0, 1, '2025-07-31 17:52:29.463092'),
(6, 'pbkdf2_sha256$1000000$qX4ftj15vlcpOi0wxDNp7T$gDSdYnA6iyGM51UYenfRVD4U3TQ9LkchJ/CsHpkWDW4=', NULL, 0, 'david_brown', 'David', 'Brown', 'david@example.com', 0, 1, '2025-07-31 17:52:30.086266'),
(7, 'pbkdf2_sha256$1000000$99Gp0Ks27QDnGmJrYw4HqN$QUbT9Rhtl09L4Y+C8SWgwGKPwp9ervR+xT4B8QxEFVc=', NULL, 0, 'lakshmanan_kumar', 'Lakshmanan', 'R', 'klakshmanan48@gmail.com', 0, 1, '2025-07-31 19:31:28.799372'),
(8, 'pbkdf2_sha256$1000000$CiloKfPcKZhtCLTTFfxGcJ$AJeg43Hq2/589BEYM82IH4upRHqHAdBr3BQQOP0zRWI=', NULL, 0, 'lakshmanan_kumar1', 'Lakshmanan', 'R', 'lakshmanan.coder@gmail.com', 0, 1, '2025-07-31 19:33:31.611954'),
(9, '!aCLfM6KAg1TcXIXdDoIWnkY1u3otwOZtx1yvzGht', NULL, 1, 'admin2', '', '', 'admin@example2.com', 1, 1, '2025-07-31 19:51:16.251903');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(9, 'modules', 'module'),
(10, 'registrations', 'registration'),
(6, 'sessions', 'session'),
(11, 'sitecore', 'contactmessage'),
(12, 'sitecore', 'systemstats'),
(7, 'students', 'otp'),
(8, 'students', 'student');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-07-31 17:50:41.986560'),
(2, 'auth', '0001_initial', '2025-07-31 17:50:42.094858'),
(3, 'admin', '0001_initial', '2025-07-31 17:50:42.118025'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-07-31 17:50:42.123151'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-07-31 17:50:42.128811'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-07-31 17:50:42.165790'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-07-31 17:50:42.187487'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-07-31 17:50:42.196484'),
(9, 'auth', '0004_alter_user_username_opts', '2025-07-31 17:50:42.201936'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-07-31 17:50:42.219023'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-07-31 17:50:42.221032'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-07-31 17:50:42.225815'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-07-31 17:50:42.235631'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-07-31 17:50:42.246361'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-07-31 17:50:42.254333'),
(16, 'auth', '0011_update_proxy_permissions', '2025-07-31 17:50:42.261947'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-07-31 17:50:42.269026'),
(18, 'modules', '0001_initial', '2025-07-31 17:50:42.277033'),
(19, 'students', '0001_initial', '2025-07-31 17:50:42.319829'),
(20, 'registrations', '0001_initial', '2025-07-31 17:50:42.363736'),
(21, 'registrations', '0002_alter_registration_grade', '2025-07-31 17:50:42.385808'),
(22, 'sessions', '0001_initial', '2025-07-31 17:50:42.403379'),
(23, 'sitecore', '0001_initial', '2025-07-31 17:50:42.422300'),
(24, 'sitecore', '0002_contactmessage_is_resolved', '2025-07-31 17:50:42.431853'),
(25, 'sitecore', '0003_alter_systemstats_options_and_more', '2025-07-31 17:50:42.467680'),
(26, 'modules', '0002_module_image_url', '2025-07-31 17:51:57.018673');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `modules_module`
--

CREATE TABLE `modules_module` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `code` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `credits` int(10) UNSIGNED NOT NULL CHECK (`credits` >= 0),
  `category` varchar(20) NOT NULL,
  `prerequisites` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `is_available_for_registration` tinyint(1) NOT NULL,
  `max_students` int(10) UNSIGNED DEFAULT NULL CHECK (`max_students` >= 0),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `image_url` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `modules_module`
--

INSERT INTO `modules_module` (`id`, `name`, `code`, `description`, `credits`, `category`, `prerequisites`, `status`, `is_available_for_registration`, `max_students`, `created_at`, `updated_at`, `image_url`) VALUES
(1, 'Introduction to Computer Science', 'CS101', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.', 3, 'core', '', 'active', 1, 30, '2025-07-31 17:52:30.652968', '2025-07-31 17:52:30.652968', 'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=800&h=600&fit=crop'),
(2, 'Advanced Mathematics', 'MATH201', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Mauris viverra venerat.', 4, 'core', '', 'active', 1, 25, '2025-07-31 17:52:30.655734', '2025-07-31 17:52:30.655734', 'https://images.unsplash.com/photo-1509228468518-180dd4864904?w=800&h=600&fit=crop'),
(3, 'English Literature', 'ENG101', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec auctor blandit quam, et molestie dolor tempus at. Nulla facilisi. Sed vel ex nec nulla tincidunt.', 3, 'elective', '', 'active', 1, 20, '2025-07-31 17:52:30.656749', '2025-07-31 17:52:30.656749', 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800&h=600&fit=crop'),
(4, 'General Physics', 'PHYS101', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras in nisi id turpis cursus vulputate. Aliquam erat volutpat. Integer posuere erat a ante venenatis dapibus.', 4, 'core', '', 'active', 1, 28, '2025-07-31 17:52:30.660691', '2025-07-31 17:52:30.660691', 'https://images.unsplash.com/photo-1636466497217-26a8cbeaf0aa?w=800&h=600&fit=crop'),
(5, 'Digital Art & Design', 'ART201', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.', 3, 'elective', '', 'active', 1, 15, '2025-07-31 17:52:30.662737', '2025-07-31 17:52:30.662737', 'https://images.unsplash.com/photo-1561998338-13ad7883b20f?w=800&h=600&fit=crop'),
(6, 'Introduction to Biology', 'BIO101', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed cursus ante dapibus diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet.', 4, 'core', '', 'active', 1, 22, '2025-07-31 17:52:30.664747', '2025-07-31 17:52:30.664747', 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=600&fit=crop');

-- --------------------------------------------------------

--
-- Table structure for table `registrations_registration`
--

CREATE TABLE `registrations_registration` (
  `id` bigint(20) NOT NULL,
  `date_registered` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `grade` varchar(5) DEFAULT NULL,
  `completion_date` datetime(6) DEFAULT NULL,
  `withdrawal_date` datetime(6) DEFAULT NULL,
  `withdrawal_reason` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `module_id` bigint(20) NOT NULL,
  `student_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `registrations_registration`
--

INSERT INTO `registrations_registration` (`id`, `date_registered`, `status`, `is_active`, `grade`, `completion_date`, `withdrawal_date`, `withdrawal_reason`, `created_at`, `updated_at`, `module_id`, `student_id`) VALUES
(1, '2025-07-31 17:52:30.670821', 'withdrawn', 1, 'A', NULL, NULL, '', '2025-07-31 17:52:30.670821', '2025-07-31 17:52:30.670821', 5, 4),
(2, '2025-07-31 17:52:30.672820', 'withdrawn', 1, NULL, NULL, NULL, '', '2025-07-31 17:52:30.672820', '2025-07-31 17:52:30.672820', 6, 4),
(3, '2025-07-31 17:52:30.674727', 'withdrawn', 1, NULL, NULL, NULL, '', '2025-07-31 17:52:30.674727', '2025-07-31 17:52:30.674727', 1, 4),
(4, '2025-07-31 17:52:30.677752', 'enrolled', 1, 'B', NULL, NULL, '', '2025-07-31 17:52:30.677752', '2025-07-31 17:52:30.677752', 5, 3),
(5, '2025-07-31 17:52:30.679142', 'enrolled', 1, NULL, NULL, NULL, '', '2025-07-31 17:52:30.679142', '2025-07-31 17:52:30.679142', 6, 3),
(6, '2025-07-31 17:52:30.681155', 'enrolled', 1, 'B', NULL, NULL, '', '2025-07-31 17:52:30.681155', '2025-07-31 17:52:30.681155', 1, 3),
(7, '2025-07-31 17:52:30.684853', 'withdrawn', 1, 'C', NULL, NULL, '', '2025-07-31 17:52:30.684853', '2025-07-31 17:52:30.684853', 5, 2),
(8, '2025-07-31 17:52:30.686863', 'completed', 1, 'A', NULL, NULL, '', '2025-07-31 17:52:30.686863', '2025-07-31 17:52:30.686863', 6, 2),
(9, '2025-07-31 17:52:30.688873', 'enrolled', 1, NULL, NULL, NULL, '', '2025-07-31 17:52:30.688873', '2025-07-31 17:52:30.688873', 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `sitecore_contactmessage`
--

CREATE TABLE `sitecore_contactmessage` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `phone` varchar(20) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `is_replied` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_resolved` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sitecore_contactmessage`
--

INSERT INTO `sitecore_contactmessage` (`id`, `name`, `email`, `subject`, `message`, `phone`, `is_read`, `is_replied`, `created_at`, `updated_at`, `is_resolved`) VALUES
(1, 'Alex Thompson', 'alex@example.com', 'Registration Question', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', '', 0, 0, '2025-07-31 17:52:30.689872', '2025-07-31 17:52:30.689872', 0),
(2, 'Maria Garcia', 'maria@example.com', 'Technical Support', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut enim ad minim veniam, quis nostrud exercitation ullamco.', '', 0, 0, '2025-07-31 17:52:30.690939', '2025-07-31 17:52:30.690939', 0);

-- --------------------------------------------------------

--
-- Table structure for table `sitecore_systemstats`
--

CREATE TABLE `sitecore_systemstats` (
  `id` bigint(20) NOT NULL,
  `total_students` int(10) UNSIGNED NOT NULL CHECK (`total_students` >= 0),
  `total_modules` int(10) UNSIGNED NOT NULL CHECK (`total_modules` >= 0),
  `total_registrations` int(10) UNSIGNED NOT NULL CHECK (`total_registrations` >= 0),
  `active_modules` int(10) UNSIGNED NOT NULL CHECK (`active_modules` >= 0),
  `last_updated` datetime(6) NOT NULL,
  `active_registrations` int(10) UNSIGNED NOT NULL CHECK (`active_registrations` >= 0),
  `completed_registrations` int(10) UNSIGNED NOT NULL CHECK (`completed_registrations` >= 0),
  `date_recorded` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sitecore_systemstats`
--

INSERT INTO `sitecore_systemstats` (`id`, `total_students`, `total_modules`, `total_registrations`, `active_modules`, `last_updated`, `active_registrations`, `completed_registrations`, `date_recorded`) VALUES
(1, 4, 6, 9, 6, '2025-07-31 19:45:33.039809', 4, 1, '2025-07-31 17:52:30.693867');

-- --------------------------------------------------------

--
-- Table structure for table `students_otp`
--

CREATE TABLE `students_otp` (
  `id` bigint(20) NOT NULL,
  `otp_code` varchar(6) NOT NULL,
  `purpose` varchar(20) NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students_otp`
--

INSERT INTO `students_otp` (`id`, `otp_code`, `purpose`, `is_used`, `created_at`, `expires_at`, `user_id`) VALUES
(1, '545050', 'verification', 0, '2025-07-31 19:31:29.259937', '2025-07-31 19:41:29.259937', 7),
(2, '343231', 'verification', 0, '2025-07-31 19:32:26.767671', '2025-07-31 19:42:26.767671', 7),
(3, '409526', 'verification', 0, '2025-07-31 19:32:51.301828', '2025-07-31 19:42:51.301828', 7),
(4, '800491', 'verification', 0, '2025-07-31 19:33:32.221564', '2025-07-31 19:43:32.220566', 8),
(5, '848617', 'verification', 0, '2025-07-31 19:35:52.701501', '2025-07-31 19:45:52.701501', 7);

-- --------------------------------------------------------

--
-- Table structure for table `students_student`
--

CREATE TABLE `students_student` (
  `id` bigint(20) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `phone` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `city` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `verification_token` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students_student`
--

INSERT INTO `students_student` (`id`, `date_of_birth`, `phone`, `address`, `city`, `country`, `photo`, `is_verified`, `verification_token`, `created_at`, `updated_at`, `user_id`) VALUES
(1, '1995-01-01', '+16835314115', '', '', '', '', 1, '', '2025-07-31 17:52:28.874718', '2025-07-31 17:52:28.874718', 3),
(2, '1995-01-01', '+19280578492', '', '', '', '', 1, '', '2025-07-31 17:52:29.460084', '2025-07-31 17:52:29.460084', 4),
(3, '1995-01-01', '+13854472144', '', '', '', '', 1, '', '2025-07-31 17:52:30.086266', '2025-07-31 17:52:30.086266', 5),
(4, '1995-01-01', '+16890150846', '', '', '', '', 1, '', '2025-07-31 17:52:30.650351', '2025-07-31 17:52:30.650351', 6),
(5, NULL, '', '', '', '', '', 0, '', '2025-07-31 19:05:25.257800', '2025-07-31 19:05:25.257800', 1),
(6, NULL, '', '', '', '', '', 0, '', '2025-07-31 19:24:20.678487', '2025-07-31 19:24:20.678487', 2),
(7, NULL, '', '', '', '', '', 0, '', '2025-07-31 19:31:29.249083', '2025-07-31 19:31:29.249083', 7),
(8, NULL, '', '', '', '', '', 0, '', '2025-07-31 19:33:32.215451', '2025-07-31 19:33:32.216498', 8);

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
-- Indexes for table `registrations_registration`
--
ALTER TABLE `registrations_registration`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `registrations_registration_student_id_module_id_efc03bd9_uniq` (`student_id`,`module_id`),
  ADD KEY `registrations_regist_module_id_f1d61892_fk_modules_m` (`module_id`);

--
-- Indexes for table `sitecore_contactmessage`
--
ALTER TABLE `sitecore_contactmessage`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sitecore_systemstats`
--
ALTER TABLE `sitecore_systemstats`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `students_otp`
--
ALTER TABLE `students_otp`
  ADD PRIMARY KEY (`id`),
  ADD KEY `students_otp_user_id_0f6356ef_fk_auth_user_id` (`user_id`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

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
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `modules_module`
--
ALTER TABLE `modules_module`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `registrations_registration`
--
ALTER TABLE `registrations_registration`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `sitecore_contactmessage`
--
ALTER TABLE `sitecore_contactmessage`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `sitecore_systemstats`
--
ALTER TABLE `sitecore_systemstats`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `students_otp`
--
ALTER TABLE `students_otp`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `students_student`
--
ALTER TABLE `students_student`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

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
-- Constraints for table `registrations_registration`
--
ALTER TABLE `registrations_registration`
  ADD CONSTRAINT `registrations_regist_module_id_f1d61892_fk_modules_m` FOREIGN KEY (`module_id`) REFERENCES `modules_module` (`id`),
  ADD CONSTRAINT `registrations_regist_student_id_4904cb27_fk_students_` FOREIGN KEY (`student_id`) REFERENCES `students_student` (`id`);

--
-- Constraints for table `students_otp`
--
ALTER TABLE `students_otp`
  ADD CONSTRAINT `students_otp_user_id_0f6356ef_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `students_student`
--
ALTER TABLE `students_student`
  ADD CONSTRAINT `students_student_user_id_56286dbb_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
