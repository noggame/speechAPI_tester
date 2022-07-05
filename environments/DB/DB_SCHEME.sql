-- Adminer 4.8.1 PostgreSQL 10.8 dump

connect "apidata";

CREATE SEQUENCE actual_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."actual" (
    "index" bigint DEFAULT nextval('actual_seq') NOT NULL,
    "result" bigint NOT NULL,
    "value" text NOT NULL,
    "registered" timestamptz NOT NULL,
    CONSTRAINT "actual_index" PRIMARY KEY ("index")
) WITH (oids = false);

CREATE SEQUENCE api_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."api" (
    "index" bigint DEFAULT nextval('api_seq') NOT NULL,
    "name" text NOT NULL,
    "provider" text NOT NULL,
    "purpose" text NOT NULL,
    "url" text NOT NULL,
    "version" text DEFAULT '1.0' NOT NULL,
    "registered" timestamptz NOT NULL,
    CONSTRAINT "api_index" PRIMARY KEY ("index"),
    CONSTRAINT "api_provider_purpose_version" UNIQUE ("provider", "purpose", "version")
) WITH (oids = false);

CREATE SEQUENCE datainfo_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 548 CACHE 1;

CREATE TABLE "public"."datainfo" (
    "index" integer DEFAULT nextval('datainfo_seq') NOT NULL,
    "title" text NOT NULL,
    "purpose" text NOT NULL,
    "origin" text,
    "base_dir" text,
    "type" text,
    "format" text,
    "registered" timestamptz NOT NULL,
    CONSTRAINT "datainfo_index" PRIMARY KEY ("index"),
    CONSTRAINT "datainfo_title_purpose" UNIQUE ("title", "purpose")
) WITH (oids = false);

COMMENT ON COLUMN "public"."datainfo"."origin" IS 'refered from';

COMMENT ON COLUMN "public"."datainfo"."type" IS 'file type (image, sound, text, ...)';

COMMENT ON COLUMN "public"."datainfo"."format" IS 'file format (jpeg, wav, mp3, txt, ...)';

COMMENT ON COLUMN "public"."datainfo"."purpose" IS 'test purpose (STT, FaceDetection, ...)';

CREATE SEQUENCE expect_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."expect" (
    "index" bigint DEFAULT nextval('expect_seq') NOT NULL,
    "testset" bigint NOT NULL,
    "value" text NOT NULL,
    "registered" timestamptz NOT NULL,
    CONSTRAINT "expect_index" PRIMARY KEY ("index")
) WITH (oids = false);

CREATE SEQUENCE key_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."key" (
    "index" bigint DEFAULT nextval('key_seq') NOT NULL,
    "api" bigint NOT NULL,
    "name" text NOT NULL,
    "value" text NOT NULL,
    "registered" timestamptz NOT NULL,
    CONSTRAINT "key_index" PRIMARY KEY ("index")
) WITH (oids = false);

CREATE SEQUENCE result_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."result" (
    "index" bigint DEFAULT nextval('result_seq') NOT NULL,
    "testset" bigint NOT NULL,
    "api" bigint NOT NULL,
    "output" text,
    "registered" timestamptz NOT NULL,
    CONSTRAINT "result_index" PRIMARY KEY ("index"),
    CONSTRAINT "result_testset_api" UNIQUE ("testset", "api")
) WITH (oids = false);

COMMENT ON COLUMN "public"."result"."output" IS 'output text or path if exist';

CREATE SEQUENCE testset_seq INCREMENT 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1;

CREATE TABLE "public"."testset" (
    "index" bigint DEFAULT nextval('testset_seq') NOT NULL,
    "source" text NOT NULL,
    "datainfo" integer NOT NULL,
    "registered" timestamptz NOT NULL,
    CONSTRAINT "testset_datainfo_source" UNIQUE ("datainfo", "source"),
    CONSTRAINT "testset_index" PRIMARY KEY ("index")
) WITH (oids = false);

ALTER TABLE ONLY "public"."actual" ADD CONSTRAINT "actual_result_fkey" FOREIGN KEY (result) REFERENCES result(index) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."expect" ADD CONSTRAINT "expect_testset_fkey" FOREIGN KEY (testset) REFERENCES testset(index) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."key" ADD CONSTRAINT "key_api_fkey" FOREIGN KEY (api) REFERENCES api(index) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."result" ADD CONSTRAINT "result_api_fkey" FOREIGN KEY (api) REFERENCES api(index) ON UPDATE RESTRICT ON DELETE RESTRICT NOT DEFERRABLE;
ALTER TABLE ONLY "public"."result" ADD CONSTRAINT "result_testset_id_fkey" FOREIGN KEY (testset) REFERENCES testset(index) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."testset" ADD CONSTRAINT "testset_datainfo_fkey" FOREIGN KEY (datainfo) REFERENCES datainfo(index) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

-- 2022-07-04 10:05:17.362739+00
