-- LeadFlow SaaS – Sprint S1 – Initial Schema
-- Supabase / PostgreSQL 15+
-- Run via: supabase db push  or  paste in Supabase SQL editor

-- ============================================================
-- EXTENSIONS
-- ============================================================
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- trigram similarity for fuzzy search

-- ============================================================
-- PROFILES  (1-to-1 with auth.users)
-- ============================================================
CREATE TABLE public.profiles (
  id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email       TEXT NOT NULL,
  full_name   TEXT,
  avatar_url  TEXT,
  plan        TEXT NOT NULL DEFAULT 'free'
                CHECK (plan IN ('free', 'starter', 'pro', 'enterprise')),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- PIPELINES
-- ============================================================
CREATE TABLE public.pipelines (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name        TEXT NOT NULL,
  description TEXT,
  stages      JSONB NOT NULL DEFAULT '[
    {"id":"new",       "name":"Nouveau",      "color":"#6366f1","order":0},
    {"id":"contacted", "name":"Contacté",     "color":"#f59e0b","order":1},
    {"id":"qualified", "name":"Qualifié",     "color":"#3b82f6","order":2},
    {"id":"proposal",  "name":"Proposition",  "color":"#8b5cf6","order":3},
    {"id":"won",       "name":"Gagné",        "color":"#10b981","order":4},
    {"id":"lost",      "name":"Perdu",        "color":"#ef4444","order":5}
  ]'::JSONB,
  is_default  BOOLEAN NOT NULL DEFAULT FALSE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- LEADS
-- ============================================================
CREATE TABLE public.leads (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id          UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Contact
  first_name       TEXT,
  last_name        TEXT,
  email            TEXT,
  email_2          TEXT,
  phone            TEXT,
  phone_2          TEXT,
  linkedin_url     TEXT,

  -- Company
  company_name     TEXT,
  company_website  TEXT,
  -- Generated: domain extracted from email (used for name+domain dedup)
  email_domain     TEXT GENERATED ALWAYS AS (
    CASE
      WHEN email IS NOT NULL AND position('@' IN email) > 0
      THEN lower(split_part(email, '@', 2))
      ELSE NULL
    END
  ) STORED,
  job_title        TEXT,
  department       TEXT,
  industry         TEXT,
  company_size     TEXT,   -- free-text: "11-50", "PME", etc.

  -- Location
  city             TEXT,
  region           TEXT,
  country          TEXT NOT NULL DEFAULT 'FR',

  -- CRM
  pipeline_id      UUID REFERENCES public.pipelines(id) ON DELETE SET NULL,
  stage            TEXT NOT NULL DEFAULT 'new',
  status           TEXT NOT NULL DEFAULT 'active'
                     CHECK (status IN ('active','inactive','unsubscribed','bounced')),
  score            SMALLINT NOT NULL DEFAULT 0 CHECK (score BETWEEN 0 AND 100),
  source           TEXT,
  tags             TEXT[]  NOT NULL DEFAULT '{}',
  notes            TEXT,

  -- Flexible extra fields from CSV
  custom_fields    JSONB NOT NULL DEFAULT '{}',

  -- Tracking
  last_contacted_at TIMESTAMPTZ,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- IMPORTS
-- ============================================================
CREATE TABLE public.imports (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id          UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  filename         TEXT NOT NULL,
  source_type      TEXT NOT NULL DEFAULT 'csv'
                     CHECK (source_type IN ('csv','google_sheet','excel','api','manual')),
  source_url       TEXT,

  total_rows       INTEGER NOT NULL DEFAULT 0,
  imported_count   INTEGER NOT NULL DEFAULT 0,
  skipped_count    INTEGER NOT NULL DEFAULT 0,
  updated_count    INTEGER NOT NULL DEFAULT 0,
  error_count      INTEGER NOT NULL DEFAULT 0,

  dedup_strategy   TEXT NOT NULL DEFAULT 'ignore'
                     CHECK (dedup_strategy IN ('ignore','merge','overwrite')),
  dedup_keys       TEXT[] NOT NULL DEFAULT '{email}',

  field_mapping    JSONB NOT NULL DEFAULT '{}',
  status           TEXT NOT NULL DEFAULT 'pending'
                     CHECK (status IN ('pending','processing','completed','failed')),
  error_log        JSONB NOT NULL DEFAULT '[]',

  created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at     TIMESTAMPTZ
);

-- ============================================================
-- IMPORT_LEADS  (junction: which leads came from which import)
-- ============================================================
CREATE TABLE public.import_leads (
  import_id   UUID NOT NULL REFERENCES public.imports(id) ON DELETE CASCADE,
  lead_id     UUID NOT NULL REFERENCES public.leads(id)   ON DELETE CASCADE,
  row_number  INTEGER,
  action      TEXT CHECK (action IN ('created','updated','skipped','error')),
  PRIMARY KEY (import_id, lead_id)
);

-- ============================================================
-- ACTIVITIES
-- ============================================================
CREATE TABLE public.activities (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id      UUID NOT NULL REFERENCES auth.users(id)  ON DELETE CASCADE,
  lead_id      UUID NOT NULL REFERENCES public.leads(id) ON DELETE CASCADE,

  type         TEXT NOT NULL
                 CHECK (type IN ('note','email','call','meeting','task','stage_change','import','linkedin')),
  title        TEXT,
  body         TEXT,
  metadata     JSONB NOT NULL DEFAULT '{}',

  scheduled_at  TIMESTAMPTZ,
  completed_at  TIMESTAMPTZ,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- INDEXES
-- ============================================================
-- Leads lookup
CREATE INDEX idx_leads_user        ON public.leads(user_id);
CREATE INDEX idx_leads_email       ON public.leads(lower(email))       WHERE email IS NOT NULL;
CREATE INDEX idx_leads_domain      ON public.leads(email_domain)       WHERE email_domain IS NOT NULL;
CREATE INDEX idx_leads_phone       ON public.leads(phone)              WHERE phone IS NOT NULL;
CREATE INDEX idx_leads_company     ON public.leads(lower(company_name)) WHERE company_name IS NOT NULL;
CREATE INDEX idx_leads_pipeline    ON public.leads(pipeline_id, stage);
CREATE INDEX idx_leads_status      ON public.leads(user_id, status);
CREATE INDEX idx_leads_tags        ON public.leads USING GIN(tags);
CREATE INDEX idx_leads_custom      ON public.leads USING GIN(custom_fields);

-- Full-text search (French + English)
CREATE INDEX idx_leads_fts ON public.leads USING GIN(
  to_tsvector('french',
    coalesce(first_name,    '') || ' ' ||
    coalesce(last_name,     '') || ' ' ||
    coalesce(company_name,  '') || ' ' ||
    coalesce(email,         '') || ' ' ||
    coalesce(job_title,     '')
  )
);

-- Activities
CREATE INDEX idx_activities_lead ON public.activities(lead_id, created_at DESC);
CREATE INDEX idx_activities_user ON public.activities(user_id, created_at DESC);

-- Imports
CREATE INDEX idx_imports_user ON public.imports(user_id, created_at DESC);

-- ============================================================
-- UPDATED_AT TRIGGER
-- ============================================================
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

CREATE TRIGGER trg_leads_updated_at
  BEFORE UPDATE ON public.leads
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_pipelines_updated_at
  BEFORE UPDATE ON public.pipelines
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TRIGGER trg_profiles_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

-- ============================================================
-- AUTO-PROVISION: profile + default pipeline on signup
-- ============================================================
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER LANGUAGE plpgsql SECURITY DEFINER SET search_path = public AS $$
DECLARE
  v_pipeline_id UUID;
BEGIN
  INSERT INTO public.profiles (id, email, full_name)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email,'@',1))
  );

  INSERT INTO public.pipelines (user_id, name, is_default)
  VALUES (NEW.id, 'Pipeline principal', TRUE)
  RETURNING id INTO v_pipeline_id;

  RETURN NEW;
END;
$$;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================================
-- DEDUPLICATION + UPSERT FUNCTION
--
-- p_dedup_strategy : 'ignore'    → skip if duplicate found
--                    'merge'     → fill only NULL/empty fields
--                    'overwrite' → update all provided fields
--
-- p_dedup_keys     : array of keys to check for duplicates
--                    'email'       → exact match on lower(email)
--                    'phone'       → normalized phone match
--                    'name+domain' → company_name + email_domain
--
-- Returns JSONB: { lead_id, action: 'created'|'updated'|'skipped' }
-- ============================================================
CREATE OR REPLACE FUNCTION public.upsert_lead(
  p_user_id        UUID,
  p_data           JSONB,
  p_dedup_strategy TEXT    DEFAULT 'ignore',
  p_dedup_keys     TEXT[]  DEFAULT ARRAY['email'],
  p_import_id      UUID    DEFAULT NULL
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER SET search_path = public
AS $$
DECLARE
  v_existing_id  UUID;
  v_lead_id      UUID;
  v_action       TEXT;
  v_email        TEXT  := lower(trim(coalesce(p_data->>'email','')));
  v_phone        TEXT  := regexp_replace(coalesce(p_data->>'phone',''), '[^0-9+]', '', 'g');
  v_company      TEXT  := lower(trim(coalesce(p_data->>'company_name','')));
  v_domain       TEXT;
BEGIN
  -- Security: caller must be the authenticated user
  IF auth.uid() IS DISTINCT FROM p_user_id THEN
    RAISE EXCEPTION 'Unauthorized';
  END IF;

  v_domain := CASE WHEN position('@' IN v_email) > 0 THEN split_part(v_email,'@',2) ELSE NULL END;

  -- ── Duplicate detection ──────────────────────────────────
  IF v_existing_id IS NULL AND 'email' = ANY(p_dedup_keys) AND v_email <> '' THEN
    SELECT id INTO v_existing_id
    FROM public.leads
    WHERE user_id = p_user_id AND lower(email) = v_email
    LIMIT 1;
  END IF;

  IF v_existing_id IS NULL AND 'phone' = ANY(p_dedup_keys) AND v_phone <> '' THEN
    SELECT id INTO v_existing_id
    FROM public.leads
    WHERE user_id = p_user_id
      AND regexp_replace(coalesce(phone,''), '[^0-9+]', '', 'g') = v_phone
    LIMIT 1;
  END IF;

  IF v_existing_id IS NULL AND 'name+domain' = ANY(p_dedup_keys)
     AND v_company <> '' AND v_domain IS NOT NULL THEN
    SELECT id INTO v_existing_id
    FROM public.leads
    WHERE user_id = p_user_id
      AND lower(company_name) = v_company
      AND email_domain = v_domain
    LIMIT 1;
  END IF;

  -- ── Apply strategy ───────────────────────────────────────
  IF v_existing_id IS NOT NULL THEN

    CASE p_dedup_strategy

      WHEN 'ignore' THEN
        v_action  := 'skipped';
        v_lead_id := v_existing_id;

      WHEN 'merge' THEN
        -- Only fill NULL / empty existing fields
        UPDATE public.leads SET
          first_name       = COALESCE(NULLIF(first_name,''),       p_data->>'first_name'),
          last_name        = COALESCE(NULLIF(last_name,''),        p_data->>'last_name'),
          email            = COALESCE(NULLIF(email,''),            p_data->>'email'),
          email_2          = COALESCE(NULLIF(email_2,''),          p_data->>'email_2'),
          phone            = COALESCE(NULLIF(phone,''),            p_data->>'phone'),
          phone_2          = COALESCE(NULLIF(phone_2,''),          p_data->>'phone_2'),
          company_name     = COALESCE(NULLIF(company_name,''),     p_data->>'company_name'),
          company_website  = COALESCE(NULLIF(company_website,''),  p_data->>'company_website'),
          job_title        = COALESCE(NULLIF(job_title,''),        p_data->>'job_title'),
          department       = COALESCE(NULLIF(department,''),       p_data->>'department'),
          linkedin_url     = COALESCE(NULLIF(linkedin_url,''),     p_data->>'linkedin_url'),
          industry         = COALESCE(NULLIF(industry,''),         p_data->>'industry'),
          company_size     = COALESCE(NULLIF(company_size,''),     p_data->>'company_size'),
          city             = COALESCE(NULLIF(city,''),             p_data->>'city'),
          region           = COALESCE(NULLIF(region,''),           p_data->>'region'),
          country          = COALESCE(NULLIF(country,'FR'),        p_data->>'country'),
          source           = COALESCE(NULLIF(source,''),           p_data->>'source'),
          notes            = COALESCE(NULLIF(notes,''),            p_data->>'notes'),
          updated_at       = now()
        WHERE id = v_existing_id;
        v_action  := 'updated';
        v_lead_id := v_existing_id;

      WHEN 'overwrite' THEN
        -- Replace all provided non-null fields
        UPDATE public.leads SET
          first_name       = COALESCE(NULLIF(p_data->>'first_name',''),      first_name),
          last_name        = COALESCE(NULLIF(p_data->>'last_name',''),       last_name),
          email            = COALESCE(NULLIF(p_data->>'email',''),           email),
          email_2          = COALESCE(NULLIF(p_data->>'email_2',''),         email_2),
          phone            = COALESCE(NULLIF(p_data->>'phone',''),           phone),
          phone_2          = COALESCE(NULLIF(p_data->>'phone_2',''),         phone_2),
          company_name     = COALESCE(NULLIF(p_data->>'company_name',''),    company_name),
          company_website  = COALESCE(NULLIF(p_data->>'company_website',''), company_website),
          job_title        = COALESCE(NULLIF(p_data->>'job_title',''),       job_title),
          department       = COALESCE(NULLIF(p_data->>'department',''),      department),
          linkedin_url     = COALESCE(NULLIF(p_data->>'linkedin_url',''),    linkedin_url),
          industry         = COALESCE(NULLIF(p_data->>'industry',''),        industry),
          company_size     = COALESCE(NULLIF(p_data->>'company_size',''),    company_size),
          city             = COALESCE(NULLIF(p_data->>'city',''),            city),
          region           = COALESCE(NULLIF(p_data->>'region',''),          region),
          country          = COALESCE(NULLIF(p_data->>'country',''),         country),
          source           = COALESCE(NULLIF(p_data->>'source',''),          source),
          notes            = COALESCE(NULLIF(p_data->>'notes',''),           notes),
          custom_fields    = custom_fields || COALESCE((p_data->'custom_fields')::JSONB, '{}'),
          updated_at       = now()
        WHERE id = v_existing_id;
        v_action  := 'updated';
        v_lead_id := v_existing_id;

    END CASE;

  ELSE
    -- ── New lead ──────────────────────────────────────────
    INSERT INTO public.leads (
      user_id, first_name, last_name, email, email_2, phone, phone_2,
      company_name, company_website, job_title, department, linkedin_url,
      industry, company_size, city, region, country, source,
      pipeline_id, stage, tags, notes, custom_fields
    ) VALUES (
      p_user_id,
      NULLIF(trim(coalesce(p_data->>'first_name','')), ''),
      NULLIF(trim(coalesce(p_data->>'last_name','')), ''),
      NULLIF(trim(coalesce(p_data->>'email','')), ''),
      NULLIF(trim(coalesce(p_data->>'email_2','')), ''),
      NULLIF(trim(coalesce(p_data->>'phone','')), ''),
      NULLIF(trim(coalesce(p_data->>'phone_2','')), ''),
      NULLIF(trim(coalesce(p_data->>'company_name','')), ''),
      NULLIF(trim(coalesce(p_data->>'company_website','')), ''),
      NULLIF(trim(coalesce(p_data->>'job_title','')), ''),
      NULLIF(trim(coalesce(p_data->>'department','')), ''),
      NULLIF(trim(coalesce(p_data->>'linkedin_url','')), ''),
      NULLIF(trim(coalesce(p_data->>'industry','')), ''),
      NULLIF(trim(coalesce(p_data->>'company_size','')), ''),
      NULLIF(trim(coalesce(p_data->>'city','')), ''),
      NULLIF(trim(coalesce(p_data->>'region','')), ''),
      COALESCE(NULLIF(trim(coalesce(p_data->>'country','')), ''), 'FR'),
      NULLIF(trim(coalesce(p_data->>'source','')), ''),
      CASE WHEN p_data->>'pipeline_id' IS NOT NULL
           THEN (p_data->>'pipeline_id')::UUID ELSE NULL END,
      COALESCE(NULLIF(p_data->>'stage',''), 'new'),
      -- tags: accept JSON array OR comma-separated string
      CASE
        WHEN p_data->'tags' IS NOT NULL AND jsonb_typeof(p_data->'tags') = 'array'
          THEN ARRAY(SELECT trim(v) FROM jsonb_array_elements_text(p_data->'tags') v WHERE trim(v) <> '')
        WHEN p_data->>'tags' IS NOT NULL AND p_data->>'tags' <> ''
          THEN ARRAY(SELECT trim(v) FROM unnest(string_to_array(p_data->>'tags',',')) v WHERE trim(v) <> '')
        ELSE '{}'::TEXT[]
      END,
      NULLIF(trim(coalesce(p_data->>'notes','')), ''),
      COALESCE((p_data->'custom_fields')::JSONB, '{}')
    )
    RETURNING id INTO v_lead_id;

    v_action := 'created';
  END IF;

  -- ── Link to import batch ─────────────────────────────────
  IF p_import_id IS NOT NULL AND v_lead_id IS NOT NULL THEN
    INSERT INTO public.import_leads (import_id, lead_id, action)
    VALUES (p_import_id, v_lead_id, v_action)
    ON CONFLICT (import_id, lead_id) DO UPDATE SET action = EXCLUDED.action;
  END IF;

  RETURN jsonb_build_object('lead_id', v_lead_id, 'action', v_action);
END;
$$;

GRANT EXECUTE ON FUNCTION public.upsert_lead TO authenticated;

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================
ALTER TABLE public.profiles     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.pipelines    ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.leads        ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.imports      ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.import_leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activities   ENABLE ROW LEVEL SECURITY;

-- Profiles: own row only
CREATE POLICY "profiles: own row"
  ON public.profiles FOR ALL
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Pipelines: own rows only
CREATE POLICY "pipelines: own rows"
  ON public.pipelines FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Leads: own rows only
CREATE POLICY "leads: own rows"
  ON public.leads FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Imports: own rows only
CREATE POLICY "imports: own rows"
  ON public.imports FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Import leads: accessible only through owned imports
CREATE POLICY "import_leads: via owned import"
  ON public.import_leads FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM public.imports i
      WHERE i.id = import_id AND i.user_id = auth.uid()
    )
  );

-- Activities: own rows only
CREATE POLICY "activities: own rows"
  ON public.activities FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);
