--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: cs280
--

CREATE OR REPLACE PROCEDURAL LANGUAGE plpgsql;


ALTER PROCEDURAL LANGUAGE plpgsql OWNER TO cs280;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO cs280;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO cs280;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO cs280;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO cs280;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_message; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE auth_message (
    id integer NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL
);


ALTER TABLE public.auth_message OWNER TO cs280;

--
-- Name: auth_message_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE auth_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_message_id_seq OWNER TO cs280;

--
-- Name: auth_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE auth_message_id_seq OWNED BY auth_message.id;


--
-- Name: auth_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('auth_message_id_seq', 1, false);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO cs280;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO cs280;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('auth_permission_id_seq', 57, true);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    password character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO cs280;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO cs280;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO cs280;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO cs280;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('auth_user_id_seq', 5, true);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO cs280;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO cs280;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 18, true);


--
-- Name: core_customtag; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE core_customtag (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL
);


ALTER TABLE public.core_customtag OWNER TO cs280;

--
-- Name: core_customtag_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE core_customtag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_customtag_id_seq OWNER TO cs280;

--
-- Name: core_customtag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE core_customtag_id_seq OWNED BY core_customtag.id;


--
-- Name: core_customtag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('core_customtag_id_seq', 4, true);


--
-- Name: core_customtagitem; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE core_customtagitem (
    id integer NOT NULL,
    object_id integer NOT NULL,
    content_type_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.core_customtagitem OWNER TO cs280;

--
-- Name: core_customtagitem_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE core_customtagitem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_customtagitem_id_seq OWNER TO cs280;

--
-- Name: core_customtagitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE core_customtagitem_id_seq OWNED BY core_customtagitem.id;


--
-- Name: core_customtagitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('core_customtagitem_id_seq', 26, true);


--
-- Name: core_note; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE core_note (
    id integer NOT NULL,
    published boolean DEFAULT true NOT NULL,
    creation_time timestamp with time zone NOT NULL,
    update_time timestamp with time zone,
    "time" timestamp with time zone,
    end_time timestamp with time zone,
    text text NOT NULL,
    user_id integer,
    video_id integer,
    link character varying(512),
    icon character varying(100),
    icon_link character varying(512),
    user_name character varying(64),
    user_link character varying(512),
    type character varying(32),
    source_link character varying(512),
    source character varying(256),
    "offset" integer,
    private boolean NOT NULL,
    original_source character varying(256),
    original_source_link character varying(512),
    original_data text,
    import_source_id integer,
    end_offset integer,
    import_source_name character varying(128)
);


ALTER TABLE public.core_note OWNER TO cs280;

--
-- Name: core_note_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE core_note_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_note_id_seq OWNER TO cs280;

--
-- Name: core_note_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE core_note_id_seq OWNED BY core_note.id;


--
-- Name: core_note_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('core_note_id_seq', 47459, true);


--
-- Name: core_source; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE core_source (
    id integer NOT NULL,
    published boolean DEFAULT true NOT NULL,
    creation_time timestamp with time zone NOT NULL,
    update_time timestamp with time zone,
    "time" timestamp with time zone,
    end_time timestamp with time zone,
    url character varying(512) NOT NULL,
    type character varying(32) DEFAULT 'twitter'::character varying NOT NULL,
    video_id integer,
    user_id integer DEFAULT 1 NOT NULL,
    scraped boolean NOT NULL,
    content character varying(100),
    twitter_user character varying(32),
    twitter_hash character varying(64),
    twitter_start_id character varying(128),
    twitter_end_id character varying(128),
    twitter_search character varying(256),
    error_message character varying(256),
    csv_data text,
    name character varying(128),
    srt_data text
);


ALTER TABLE public.core_source OWNER TO cs280;

--
-- Name: core_source_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE core_source_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_source_id_seq OWNER TO cs280;

--
-- Name: core_source_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE core_source_id_seq OWNED BY core_source.id;


--
-- Name: core_source_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('core_source_id_seq', 93, true);


--
-- Name: core_userprofile; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE core_userprofile (
    id integer NOT NULL,
    user_id integer NOT NULL,
    accepted_eula boolean DEFAULT false NOT NULL,
    can_note boolean DEFAULT false NOT NULL,
    role character varying(32) DEFAULT 'user'::character varying
);


ALTER TABLE public.core_userprofile OWNER TO cs280;

--
-- Name: core_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE core_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_userprofile_id_seq OWNER TO cs280;

--
-- Name: core_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE core_userprofile_id_seq OWNED BY core_userprofile.id;


--
-- Name: core_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('core_userprofile_id_seq', 1, false);


--
-- Name: core_video; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE core_video (
    id integer NOT NULL,
    published boolean DEFAULT true NOT NULL,
    creation_time timestamp with time zone NOT NULL,
    update_time timestamp with time zone,
    "time" timestamp with time zone,
    end_time timestamp with time zone,
    title character varying(256) NOT NULL,
    description text NOT NULL,
    teaser text NOT NULL,
    video_url character varying(256) NOT NULL,
    video_file character varying(512),
    user_id integer,
    type character varying(32) NOT NULL,
    user_name character varying(64) NOT NULL,
    user_link character varying(200) NOT NULL,
    icon character varying(512),
    icon_link character varying(200) NOT NULL,
    slug character varying(256) NOT NULL,
    video_length integer,
    private boolean NOT NULL,
    lock_notes boolean NOT NULL
);


ALTER TABLE public.core_video OWNER TO cs280;

--
-- Name: core_video_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE core_video_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.core_video_id_seq OWNER TO cs280;

--
-- Name: core_video_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE core_video_id_seq OWNED BY core_video.id;


--
-- Name: core_video_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('core_video_id_seq', 149, true);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO cs280;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO cs280;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 6499, true);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO cs280;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO cs280;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('django_content_type_id_seq', 19, true);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO cs280;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO cs280;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO cs280;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Name: south_migrationhistory; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE south_migrationhistory (
    id integer NOT NULL,
    app_name character varying(255) NOT NULL,
    migration character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.south_migrationhistory OWNER TO cs280;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE south_migrationhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.south_migrationhistory_id_seq OWNER TO cs280;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE south_migrationhistory_id_seq OWNED BY south_migrationhistory.id;


--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('south_migrationhistory_id_seq', 25, true);


--
-- Name: taggit_tag; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE taggit_tag (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL
);


ALTER TABLE public.taggit_tag OWNER TO cs280;

--
-- Name: taggit_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE taggit_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taggit_tag_id_seq OWNER TO cs280;

--
-- Name: taggit_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE taggit_tag_id_seq OWNED BY taggit_tag.id;


--
-- Name: taggit_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('taggit_tag_id_seq', 1, false);


--
-- Name: taggit_taggeditem; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE taggit_taggeditem (
    id integer NOT NULL,
    tag_id integer NOT NULL,
    object_id integer NOT NULL,
    content_type_id integer NOT NULL
);


ALTER TABLE public.taggit_taggeditem OWNER TO cs280;

--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE taggit_taggeditem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.taggit_taggeditem_id_seq OWNER TO cs280;

--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE taggit_taggeditem_id_seq OWNED BY taggit_taggeditem.id;


--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('taggit_taggeditem_id_seq', 1, false);


--
-- Name: tastypie_apiaccess; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE tastypie_apiaccess (
    id integer NOT NULL,
    identifier character varying(255) NOT NULL,
    url character varying(255) DEFAULT ''::character varying NOT NULL,
    request_method character varying(10) DEFAULT ''::character varying NOT NULL,
    accessed integer NOT NULL,
    CONSTRAINT tastypie_apiaccess_accessed_check CHECK ((accessed >= 0))
);


ALTER TABLE public.tastypie_apiaccess OWNER TO cs280;

--
-- Name: tastypie_apiaccess_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE tastypie_apiaccess_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tastypie_apiaccess_id_seq OWNER TO cs280;

--
-- Name: tastypie_apiaccess_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE tastypie_apiaccess_id_seq OWNED BY tastypie_apiaccess.id;


--
-- Name: tastypie_apiaccess_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('tastypie_apiaccess_id_seq', 1, false);


--
-- Name: tastypie_apikey; Type: TABLE; Schema: public; Owner: cs280; Tablespace: 
--

CREATE TABLE tastypie_apikey (
    id integer NOT NULL,
    user_id integer NOT NULL,
    key character varying(256) DEFAULT ''::character varying NOT NULL,
    created timestamp with time zone DEFAULT '2012-06-28 11:29:36.925986-04'::timestamp with time zone NOT NULL
);


ALTER TABLE public.tastypie_apikey OWNER TO cs280;

--
-- Name: tastypie_apikey_id_seq; Type: SEQUENCE; Schema: public; Owner: cs280
--

CREATE SEQUENCE tastypie_apikey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tastypie_apikey_id_seq OWNER TO cs280;

--
-- Name: tastypie_apikey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cs280
--

ALTER SEQUENCE tastypie_apikey_id_seq OWNED BY tastypie_apikey.id;


--
-- Name: tastypie_apikey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cs280
--

SELECT pg_catalog.setval('tastypie_apikey_id_seq', 1, false);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE auth_message ALTER COLUMN id SET DEFAULT nextval('auth_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE core_customtag ALTER COLUMN id SET DEFAULT nextval('core_customtag_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE core_customtagitem ALTER COLUMN id SET DEFAULT nextval('core_customtagitem_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE core_note ALTER COLUMN id SET DEFAULT nextval('core_note_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE core_source ALTER COLUMN id SET DEFAULT nextval('core_source_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE core_userprofile ALTER COLUMN id SET DEFAULT nextval('core_userprofile_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE core_video ALTER COLUMN id SET DEFAULT nextval('core_video_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE south_migrationhistory ALTER COLUMN id SET DEFAULT nextval('south_migrationhistory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE taggit_tag ALTER COLUMN id SET DEFAULT nextval('taggit_tag_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE taggit_taggeditem ALTER COLUMN id SET DEFAULT nextval('taggit_taggeditem_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE tastypie_apiaccess ALTER COLUMN id SET DEFAULT nextval('tastypie_apiaccess_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: cs280
--

ALTER TABLE tastypie_apikey ALTER COLUMN id SET DEFAULT nextval('tastypie_apikey_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_message; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY auth_message (id, user_id, message) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add message	4	add_message
11	Can change message	4	change_message
12	Can delete message	4	delete_message
13	Can add session	5	add_session
14	Can change session	5	change_session
15	Can delete session	5	delete_session
16	Can add content type	6	add_contenttype
17	Can change content type	6	change_contenttype
18	Can delete content type	6	delete_contenttype
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add log entry	8	add_logentry
23	Can change log entry	8	change_logentry
24	Can delete log entry	8	delete_logentry
25	Can add migration history	9	add_migrationhistory
26	Can change migration history	9	change_migrationhistory
27	Can delete migration history	9	delete_migrationhistory
28	Can add video	10	add_video
29	Can change video	10	change_video
30	Can delete video	10	delete_video
31	Can add note	11	add_note
32	Can change note	11	change_note
33	Can delete note	11	delete_note
34	Can add Kitchen Tag	12	add_customtag
35	Can change Kitchen Tag	12	change_customtag
36	Can delete Kitchen Tag	12	delete_customtag
37	Can add custom tag item	13	add_customtagitem
38	Can change custom tag item	13	change_customtagitem
39	Can delete custom tag item	13	delete_customtagitem
40	Can add source	14	add_source
41	Can change source	14	change_source
42	Can delete source	14	delete_source
43	Can add user profile	15	add_userprofile
44	Can change user profile	15	change_userprofile
45	Can delete user profile	15	delete_userprofile
46	Can add Tag	16	add_tag
47	Can change Tag	16	change_tag
48	Can delete Tag	16	delete_tag
49	Can add Tagged Item	17	add_taggeditem
50	Can change Tagged Item	17	change_taggeditem
51	Can delete Tagged Item	17	delete_taggeditem
52	Can add api access	18	add_apiaccess
53	Can change api access	18	change_apiaccess
54	Can delete api access	18	delete_apiaccess
55	Can add api key	19	add_apikey
56	Can change api key	19	change_apikey
57	Can delete api key	19	delete_apikey
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
5	admin	Administrator		info@reporterslab.org	sha1$5fb97$5749b9377b1271134ec25559a48bbbea27529d68	t	t	t	2012-07-31 09:14:09.454475-04	2012-07-31 09:13:31-04
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: core_customtag; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY core_customtag (id, name, slug) FROM stdin;
3	youtube	youtube
4	gop	gop
\.


--
-- Data for Name: core_customtagitem; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY core_customtagitem (id, object_id, content_type_id, tag_id) FROM stdin;
\.


--
-- Data for Name: core_note; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY core_note (id, published, creation_time, update_time, "time", end_time, text, user_id, video_id, link, icon, icon_link, user_name, user_link, type, source_link, source, "offset", private, original_source, original_source_link, original_data, import_source_id, end_offset, import_source_name) FROM stdin;
\.


--
-- Data for Name: core_source; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY core_source (id, published, creation_time, update_time, "time", end_time, url, type, video_id, user_id, scraped, content, twitter_user, twitter_hash, twitter_start_id, twitter_end_id, twitter_search, error_message, csv_data, name, srt_data) FROM stdin;
\.


--
-- Data for Name: core_userprofile; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY core_userprofile (id, user_id, accepted_eula, can_note, role) FROM stdin;
\.


--
-- Data for Name: core_video; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY core_video (id, published, creation_time, update_time, "time", end_time, title, description, teaser, video_url, video_file, user_id, type, user_name, user_link, icon, icon_link, slug, video_length, private, lock_notes) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
6478	2012-07-31 09:15:01.502667-04	5	10	149	Video: 2012 State Of The Union Address: Enhanced Version	3	
6479	2012-07-31 09:15:01.555771-04	5	10	148	Video: Google+ Hangouts for Media	3	
6480	2012-07-31 09:15:01.557215-04	5	10	147	Video: Google+: Broadcast Your Hangout To The World	3	
6481	2012-07-31 09:15:01.558492-04	5	10	146	Video: San Diego City Council, April 24th 	3	
6482	2012-07-31 09:15:01.559872-04	5	10	105	Video: Iridescent MP3	3	
6483	2012-07-31 09:15:01.561116-04	5	10	104	Video: NIN Ghosts 2 - 15	3	
6484	2012-07-31 09:15:01.562585-04	5	10	103	Video: The Twilight Saga Breaking Dawn Part 2: Oficial Teaser Trailer - 2012 - HD	3	
6485	2012-07-31 09:15:01.563756-04	5	10	97	Video: Double Fine Adventure Kickstarter Promotional	3	
6486	2012-07-31 09:15:01.564962-04	5	10	96	Video: o0o Twisted Destiny Minecraft Server 1.2 o0o	3	
6487	2012-07-31 09:15:01.566255-04	5	10	94	Video: San Diego City Council	3	
6488	2012-07-31 09:15:01.567745-04	5	10	93	Video: Nirvana - Come As You Are	3	
6489	2012-07-31 09:15:01.568926-04	5	10	92	Video: Newsit Tech Apple Mac OS X Mountain Lion - Tour	3	
6490	2012-07-31 09:15:01.570135-04	5	10	67	Video: Iron Sky MP4	3	
6491	2012-07-31 09:15:01.571279-04	5	10	64	Video: The Amazing Spider-Man New Trailer 2 Official 2012 [1080 HD] - Andrew Garfield	3	
6492	2012-07-31 09:15:01.572594-04	5	10	19	Video: At Twitter, The Future is Silly	3	
6493	2012-07-31 09:15:01.573915-04	5	10	6	Video: Game of Thrones 2!	3	
6494	2012-07-31 09:15:01.57491-04	5	10	5	Video: 2012 SOTU	3	
6495	2012-07-31 09:15:01.575956-04	5	10	2	Video: The Fox News/Google Debate	3	
6496	2012-07-31 09:15:59.599441-04	5	3	1	charlie	3	
6497	2012-07-31 09:15:59.602429-04	5	3	2	cs280	3	
6498	2012-07-31 09:15:59.603706-04	5	3	4	newUser	3	
6499	2012-07-31 09:15:59.605065-04	5	3	3	tester	3	
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	permission	auth	permission
2	group	auth	group
3	user	auth	user
4	message	auth	message
5	session	sessions	session
6	content type	contenttypes	contenttype
7	site	sites	site
8	log entry	admin	logentry
9	migration history	south	migrationhistory
10	video	core	video
11	note	core	note
12	Kitchen Tag	core	customtag
13	custom tag item	core	customtagitem
14	source	core	source
15	user profile	core	userprofile
16	Tag	taggit	tag
17	Tagged Item	taggit	taggeditem
18	api access	tastypie	apiaccess
19	api key	tastypie	apikey
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
6832cb3502dc7e635283742a5971c40e	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2011-10-26 14:25:24.984071-04
3b528eaedaa210b92cdf9c07dffd6f4e	YzJlMmMxMjlhN2Q5MDU5NzRhZmUxZDIxZDVhYzMxYzZkYzAzNWZjZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-02-09 17:44:22.575865-05
a2940c01750c25c2471aa805e50244e7	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-02-21 15:59:19.048176-05
467daa5fe8dfd3a0fab446dce3828960	YzJlMmMxMjlhN2Q5MDU5NzRhZmUxZDIxZDVhYzMxYzZkYzAzNWZjZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-02-13 16:12:34.575139-05
ae68795ca32232f52b9a4582b3e673e7	MmJhOTY3ZDhiMjQwNmFjOWU0YWFhNmYzZjZiMmVhNWJiYzlmMGU4NDqAAn1xAS4=\n	2012-02-23 15:17:47.592705-05
6f5a670843977989b0b0c793fa13855a	YTZjYWQxZjJjZmIyYzZkMjZmMmMxYWUxMzBjMmZjYWRjZTMxMTdmMTqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRLAVUSX2F1dGhfdXNlcl9iYWNrZW5kVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRz\nLk1vZGVsQmFja2VuZHECdS4=\n	2012-02-14 11:44:59.403302-05
7f3a311282ceaf656574728f71cfad38	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-02-23 15:18:09.090359-05
078b15a71e49ecc5456dbf5adc3f042c	YzJlMmMxMjlhN2Q5MDU5NzRhZmUxZDIxZDVhYzMxYzZkYzAzNWZjZTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-02-15 16:17:40.81033-05
55c3ae6adbcea04e1721921edcafab31	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-04-25 12:56:39.601559-04
63bac55ab4f9c1c7d1b322e1d5eeb297	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-02-28 11:51:20.593273-05
226a88ad67b6f602085cd01a26c80fd4	MmJhOTY3ZDhiMjQwNmFjOWU0YWFhNmYzZjZiMmVhNWJiYzlmMGU4NDqAAn1xAS4=\n	2012-02-28 14:44:02.789386-05
7ee882888175ad67ea0bec61b7ab494a	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-02-29 15:36:39.122351-05
91ffe64dfe5e9afa166d1b99744d0968	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-03-01 16:23:40.316846-05
8517653cbdf65632aff5123100b30069	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-03-08 23:58:16.903561-05
d145d373d4dd0365bfca378d2fa4668c	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-05-07 14:01:24.457632-04
6b8a5fa5d4744789b055eec6abb58efd	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-04-04 15:38:28.184302-04
5be4ff77806e63bb0b8d73f9d390e93f	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-05-09 16:41:24.052617-04
572f14feb5e17ab1a77d107e922c32fe	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-05-28 14:13:28.323802-04
9087a4719cfe8fa587a46816e968b1eb	NzU4ZjRjYWI2Yjk5YjI3NzY5ZDhmNDk0NmExMDM1YjcxY2M5NTFiZDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-06-04 16:23:38.929441-04
d56b30376c125136aab64a7f6bd6fc89	YTZjYWQxZjJjZmIyYzZkMjZmMmMxYWUxMzBjMmZjYWRjZTMxMTdmMTqAAn1xAShVDV9hdXRoX3Vz\nZXJfaWRLAVUSX2F1dGhfdXNlcl9iYWNrZW5kVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRz\nLk1vZGVsQmFja2VuZHECdS4=\n	2012-07-12 11:44:54.700067-04
57a4200c7ce43b2e080edb4cdb2363cc	NTY2Njk3ODY5NzNlNzNkNmE2NmZjY2Y4NWI3NTMxY2Q5MGZkZjRjNTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLBXUu\n	2012-08-14 09:14:09.457859-04
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: south_migrationhistory; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY south_migrationhistory (id, app_name, migration, applied) FROM stdin;
1	core	0001_initial	2011-10-12 19:23:03.227584-04
2	core	0002_auto__add_field_note_link__add_field_note_icon__add_field_note_icon_li	2011-10-13 18:09:35.962153-04
3	core	0003_auto__del_field_video_byline__add_field_video_user__add_field_video_ty	2011-10-14 19:30:24.042936-04
4	core	0004_auto__chg_field_note_user_link__chg_field_note_link__chg_field_note_us	2011-10-14 19:49:53.939365-04
5	core	0005_auto__add_field_note_type	2011-10-14 22:41:31.115015-04
6	core	0006_auto__add_field_note_source_link__add_field_note_source	2011-10-14 22:43:20.260012-04
7	core	0007_auto__chg_field_note_user_link__chg_field_note_link__chg_field_note_so	2011-10-17 17:49:03.585413-04
8	core	0008_auto__add_field_video_slug	2011-10-17 18:20:20.632138-04
9	core	0009_auto__chg_field_video_update_time__chg_field_note_update_time	2011-10-19 19:35:48.398172-04
10	core	0010_auto__add_field_video_video_length__add_field_note_offset	2011-10-21 16:36:00.992206-04
11	core	0011_auto__chg_field_video_time__chg_field_note_time	2011-10-21 16:50:30.484437-04
12	core	0012_auto__add_userprofile__add_field_video_private__add_field_video_lock_n	2012-01-26 23:44:03.16218-05
13	core	0013_auto__add_source__chg_field_video_video_url__chg_field_note_source_lin	2012-01-26 23:44:03.390849-05
14	core	0014_auto__add_field_source_scraped__add_field_source_content	2012-01-26 23:44:03.435262-05
15	core	0015_auto__add_unique_video_video_url	2012-01-26 23:44:03.462934-05
16	core	0016_auto__add_field_note_original_source__add_field_note_original_source_l	2012-02-08 19:41:15.383011-05
17	core	0017_auto__add_field_source_error_message	2012-02-08 20:46:57.242138-05
18	core	0018_auto__add_field_source_csv_data	2012-02-08 21:39:25.899767-05
19	core	0019_auto__chg_field_video_video_file__chg_field_video_icon__add_field_note	2012-03-16 14:25:17.065893-04
20	core	0020_auto__chg_field_note_link__chg_field_source_user	2012-03-19 19:33:56.776192-04
21	core	0021_auto__add_field_source_name	2012-03-19 20:51:41.854404-04
22	core	0022_auto__add_field_note_end_offset	2012-04-18 16:57:03.729314-04
23	core	0023_auto__add_field_source_srt_data	2012-05-15 17:10:51.396285-04
24	core	0024_auto__add_field_note_import_source_name	2012-05-21 20:36:34.590563-04
25	tastypie	0001_initial	2012-06-28 15:29:37.613935-04
\.


--
-- Data for Name: taggit_tag; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY taggit_tag (id, name, slug) FROM stdin;
\.


--
-- Data for Name: taggit_taggeditem; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY taggit_taggeditem (id, tag_id, object_id, content_type_id) FROM stdin;
\.


--
-- Data for Name: tastypie_apiaccess; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY tastypie_apiaccess (id, identifier, url, request_method, accessed) FROM stdin;
\.


--
-- Data for Name: tastypie_apikey; Type: TABLE DATA; Schema: public; Owner: cs280
--

COPY tastypie_apikey (id, user_id, key, created) FROM stdin;
\.


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_message_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: core_customtag_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY core_customtag
    ADD CONSTRAINT core_customtag_pkey PRIMARY KEY (id);


--
-- Name: core_customtag_slug_key; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY core_customtag
    ADD CONSTRAINT core_customtag_slug_key UNIQUE (slug);


--
-- Name: core_customtagitem_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY core_customtagitem
    ADD CONSTRAINT core_customtagitem_pkey PRIMARY KEY (id);


--
-- Name: core_note_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY core_note
    ADD CONSTRAINT core_note_pkey PRIMARY KEY (id);


--
-- Name: core_source_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY core_source
    ADD CONSTRAINT core_source_pkey PRIMARY KEY (id);


--
-- Name: core_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY core_userprofile
    ADD CONSTRAINT core_userprofile_pkey PRIMARY KEY (id);


--
-- Name: core_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY core_userprofile
    ADD CONSTRAINT core_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: core_video_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY core_video
    ADD CONSTRAINT core_video_pkey PRIMARY KEY (id);


--
-- Name: core_video_slug_key; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY core_video
    ADD CONSTRAINT core_video_slug_key UNIQUE (slug);


--
-- Name: core_video_video_url_uniq; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY core_video
    ADD CONSTRAINT core_video_video_url_uniq UNIQUE (video_url);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_model_key; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: south_migrationhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY south_migrationhistory
    ADD CONSTRAINT south_migrationhistory_pkey PRIMARY KEY (id);


--
-- Name: taggit_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_pkey PRIMARY KEY (id);


--
-- Name: taggit_tag_slug_key; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_slug_key UNIQUE (slug);


--
-- Name: taggit_taggeditem_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_pkey PRIMARY KEY (id);


--
-- Name: tastypie_apiaccess_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY tastypie_apiaccess
    ADD CONSTRAINT tastypie_apiaccess_pkey PRIMARY KEY (id);


--
-- Name: tastypie_apikey_pkey; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY tastypie_apikey
    ADD CONSTRAINT tastypie_apikey_pkey PRIMARY KEY (id);


--
-- Name: tastypie_apikey_user_id_key; Type: CONSTRAINT; Schema: public; Owner: cs280; Tablespace: 
--

ALTER TABLE ONLY tastypie_apikey
    ADD CONSTRAINT tastypie_apikey_user_id_key UNIQUE (user_id);


--
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_message_user_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX auth_message_user_id ON auth_message USING btree (user_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- Name: core_customtagitem_content_type_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX core_customtagitem_content_type_id ON core_customtagitem USING btree (content_type_id);


--
-- Name: core_customtagitem_object_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX core_customtagitem_object_id ON core_customtagitem USING btree (object_id);


--
-- Name: core_customtagitem_tag_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX core_customtagitem_tag_id ON core_customtagitem USING btree (tag_id);


--
-- Name: core_note_import_source_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX core_note_import_source_id ON core_note USING btree (import_source_id);


--
-- Name: core_note_user_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX core_note_user_id ON core_note USING btree (user_id);


--
-- Name: core_note_video_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX core_note_video_id ON core_note USING btree (video_id);


--
-- Name: core_source_user_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX core_source_user_id ON core_source USING btree (user_id);


--
-- Name: core_source_video_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX core_source_video_id ON core_source USING btree (video_id);


--
-- Name: core_video_user_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX core_video_user_id ON core_video USING btree (user_id);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX django_session_expire_date ON django_session USING btree (expire_date);


--
-- Name: taggit_taggeditem_content_type_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX taggit_taggeditem_content_type_id ON taggit_taggeditem USING btree (content_type_id);


--
-- Name: taggit_taggeditem_object_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX taggit_taggeditem_object_id ON taggit_taggeditem USING btree (object_id);


--
-- Name: taggit_taggeditem_tag_id; Type: INDEX; Schema: public; Owner: cs280; Tablespace: 
--

CREATE INDEX taggit_taggeditem_tag_id ON taggit_taggeditem USING btree (tag_id);


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_10c1fe6aa543e918; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY core_customtagitem
    ADD CONSTRAINT content_type_id_refs_id_10c1fe6aa543e918 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_728de91f; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_728de91f FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_3cea63fe; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT group_id_refs_id_3cea63fe FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: import_source_id_refs_id_5c7acf33f8b223e2; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY core_note
    ADD CONSTRAINT import_source_id_refs_id_5c7acf33f8b223e2 FOREIGN KEY (import_source_id) REFERENCES core_source(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tag_id_refs_id_68bc859553e41e20; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY core_customtagitem
    ADD CONSTRAINT tag_id_refs_id_68bc859553e41e20 FOREIGN KEY (tag_id) REFERENCES core_customtag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taggit_taggeditem_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taggit_taggeditem_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES taggit_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_2977677d13c8fc69; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY core_note
    ADD CONSTRAINT user_id_refs_id_2977677d13c8fc69 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_332d09f456bfdb62; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY tastypie_apikey
    ADD CONSTRAINT user_id_refs_id_332d09f456bfdb62 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_51f774de55007184; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY core_userprofile
    ADD CONSTRAINT user_id_refs_id_51f774de55007184 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_5ef48a94b76edc05; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY core_video
    ADD CONSTRAINT user_id_refs_id_5ef48a94b76edc05 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_831107f1; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT user_id_refs_id_831107f1 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_ac6593ed654534; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY core_source
    ADD CONSTRAINT user_id_refs_id_ac6593ed654534 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_f2045483; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT user_id_refs_id_f2045483 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: video_id_refs_id_1dac79624c722f7f; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY core_note
    ADD CONSTRAINT video_id_refs_id_1dac79624c722f7f FOREIGN KEY (video_id) REFERENCES core_video(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: video_id_refs_id_74f6eafff3b3f9aa; Type: FK CONSTRAINT; Schema: public; Owner: cs280
--

ALTER TABLE ONLY core_source
    ADD CONSTRAINT video_id_refs_id_74f6eafff3b3f9aa FOREIGN KEY (video_id) REFERENCES core_video(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: cs280
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM cs280;
GRANT ALL ON SCHEMA public TO cs280;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

