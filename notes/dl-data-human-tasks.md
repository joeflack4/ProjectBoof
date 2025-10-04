# Human Tasks for Data Source Access Setup

This document outlines the specific tasks that require human action to acquire and access data from each of the 7 genomic data sources. Tasks are organized by data source in priority order.

---

## cBioPortal

### Account/Access Setup
- **Required**: ❌ None
- **Optional**: ❌ None

### Tasks
1. **No human setup required** - cBioPortal is fully open access
   - Web interface: Immediately accessible at https://www.cbioportal.org
   - API: Publicly accessible, no authentication required
   - Data downloads: Available through web interface without login

### Notes
- Completely free and open source
- No registration, API keys, or authentication needed
- Can start using immediately

---

## ClinGen

### Account/Access Setup
- **Required**: ❌ None (for most use cases)
- **Optional**: ✅ Allele Registry account (if registering new alleles)

### Tasks

#### For Data Downloads and Browsing (No Action Required)
1. **No setup required** for:
   - Web browsing at https://clinicalgenome.org
   - FTP downloads from ftp://ftp.clinicalgenome.org
   - File downloads from https://search.clinicalgenome.org/kb/downloads
   - Allele Registry queries

#### For Allele Registry Registration (Optional - Only if Submitting Data)
If you need to register NEW alleles (not required for querying):

1. **Email Request** ✉️
   - Send email to: `brl-allele-reg@bcm.edu`
   - Subject: "Allele Registry Account Request"
   - Include:
     - Your name
     - Institution/organization
     - Preferred login name
     - Intended use case
   - Wait for credentials to be sent back

2. **Test Login**
   - Verify credentials work at https://reg.clinicalgenome.org
   - Save credentials securely

### Notes
- All curated data is CC0 public domain - no restrictions
- Most use cases don't require any account
- API for downloads is coming soon (no current registration needed)

---

## ClinVar

### Account/Access Setup
- **Required**: ❌ None (for data access)
- **Optional**: ✅ NCBI Submission Portal account (if submitting variants)

### Tasks

#### For Data Access (No Action Required)
1. **No setup required** for:
   - Web browsing at https://www.ncbi.nlm.nih.gov/clinvar/
   - FTP downloads from ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/
   - E-utilities API queries
   - VCF/XML/TSV file downloads

#### For Variant Submission (Optional - Only if Submitting Data)
If you plan to submit variant interpretations:

1. **Create NCBI Account** 👤
   - Go to: https://www.ncbi.nlm.nih.gov/account/
   - Click "Register for an NCBI account"
   - Provide: Email, username, password
   - Verify email address

2. **Set Up Submission Portal Account** 🔐
   - Navigate to: https://submit.ncbi.nlm.nih.gov/
   - Log in with NCBI account
   - Complete organization information
   - Request API key if doing programmatic submissions
   - Save API key securely (64-character alphanumeric)

### Notes
- ClinVar data is US Government work (public domain)
- No fees or restrictions for data access
- Submission requires account but is also free

---

## COSMIC

### Account/Access Setup
- **Required**: ✅ COSMIC account (for downloads)
- **Conditional**: ✅ Commercial license (if commercial use)

### Tasks

#### Step 1: Determine License Type 🔍
**Question**: Is your use case commercial?

**Commercial use includes:**
- Research in a for-profit company
- Creating commercial products/services
- Patient services or clinical reporting in commercial setting
- Integration into commercial software

**If YES → Commercial license required (proceed to Commercial path)**
**If NO → Academic license (free, proceed to Academic path)**

---

#### Academic/Non-Profit Path (FREE)

1. **Register for COSMIC Account** 👤
   - Go to: https://cancer.sanger.ac.uk/cosmic
   - Click "Register" or "Sign Up"
   - Provide:
     - Full name
     - **Institutional/academic email** (required - .edu, .ac.uk, etc.)
     - Institution name
     - Country
     - Password
   - Agree to academic use terms
   - Verify email address

2. **Re-register if Existing User** 🔄
   - Note: As of April 2nd, existing users must re-register
   - Use the same registration process above
   - Your previous data access will be restored

3. **Test Login and Download** ✅
   - Log in at https://cancer.sanger.ac.uk/cosmic
   - Navigate to Downloads page
   - Verify you can access download links
   - Note your credentials for download scripts

4. **Set Up Download Authentication** 💻
   - Your email and password will be needed for authenticated downloads
   - Example usage in scripts:
     ```bash
     curl -u "your-email@institution.edu:your-password" \
       -o file.vcf.gz \
       https://cancer.sanger.ac.uk/cosmic/file_download/...
     ```

---

#### Commercial Path (PAID)

1. **Register for COSMIC Account** 👤
   - Go to: https://cancer.sanger.ac.uk/cosmic
   - Click "Register"
   - Use **business email** (not personal email)
   - Complete registration form
   - Indicate commercial/business affiliation

2. **Contact COSMIC Commercial Team** 📧
   - COSMIC team will automatically contact you based on business email domain
   - If not contacted within 2 business days, email: `licensing@oncokb.org`
   - Alternatively contact via QIAGEN: https://digitalinsights.qiagen.com/products-overview/cosmic/

3. **Provide Use Case Information** 📋
   - Be prepared to describe:
     - Your company size (small, medium, large enterprise)
     - Intended use of COSMIC data
     - Expected annual report volume (if clinical use)
     - Whether using for product development
     - Geographic regions of operation

4. **Review License Agreement** 📄
   - COSMIC/QIAGEN will send license agreement
   - Review terms carefully
   - Note annual license fee (pricing varies by company size and use)
   - Legal review may be needed at your organization

5. **Execute License** ✍️
   - Sign license agreement
   - Arrange payment for annual fee
   - Provide any required documentation
   - Wait for license activation

6. **Receive Access Credentials** 🔑
   - Once license is executed and payment processed
   - Download credentials will be activated
   - Test download access

---

### Estimated Timeline
- **Academic**: 10-30 minutes (immediate access after email verification)
- **Commercial**: 1-4 weeks (depends on license negotiation)

### Notes
- Keep login credentials secure
- Academic users: Do NOT use COSMIC data for commercial purposes
- Commercial users: Ensure all team members are aware of license terms
- SFTP access is deprecated; use HTTPS downloads

---

## GenCC

### Account/Access Setup
- **Required**: ❌ None
- **Optional**: ✅ Email signup for API notifications

### Tasks

#### For Data Access (No Action Required)
1. **No setup required** for:
   - Web browsing at https://search.thegencc.org
   - File downloads (XLSX, XLS, TSV, CSV)
   - All current functionality

#### Optional: Sign Up for API Notifications
If you want to be notified when API access is available:

1. **Sign Up for Updates** 📬
   - Go to: https://thegencc.org
   - Look for "API Coming Soon" or "Stay Informed" section
   - Provide email address
   - Confirm subscription

### Notes
- Completely free, CC0 public domain
- No registration required for current access
- API is coming soon (date TBD)

---

## OncoKB

### Account/Access Setup
- **Required**: ✅ OncoKB account
- **Conditional**: ✅ Commercial license (if commercial use)

### Tasks

#### Step 1: Determine License Type 🔍
**Question**: Is your use case commercial or academic?

**Commercial use includes:**
- Research in a for-profit company
- Commercial product development
- Patient services/clinical reporting
- Integration into commercial platforms

**Academic use includes:**
- Research in academic/educational institution
- Non-profit research
- Educational purposes

---

#### Academic/Non-Profit Path (FREE)

1. **Register for OncoKB Account** 👤
   - Go to: https://www.oncokb.org
   - Click "Register" or "Sign In" → "Register"
   - Provide:
     - Full name
     - **Institutional email** (.edu, .ac.uk, etc.) - REQUIRED
     - Institution name
     - Password
   - Agree to academic license terms

2. **Verify Email** ✉️
   - Check inbox for verification email
   - Click verification link
   - Confirm email is verified

3. **Obtain API Token** 🔑
   - Log in to OncoKB
   - Navigate to "Account" or "API/License" page
   - Generate API token
   - **SAVE TOKEN SECURELY** (cannot be viewed again)
   - Token format: Long alphanumeric string
   - Example: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

4. **Test API Access** ✅
   - Try a simple API query:
     ```bash
     curl -X GET "https://www.oncokb.org/api/v1/genes" \
       -H "Authorization: Bearer YOUR_TOKEN_HERE"
     ```
   - Verify successful response

5. **Set Up Environment Variable** 💻
   - Store token in environment variable (recommended):
     ```bash
     export ONCOKB_TOKEN="your-token-here"
     ```
   - Or add to `.bashrc` / `.zshrc`:
     ```bash
     echo 'export ONCOKB_TOKEN="your-token-here"' >> ~/.bashrc
     ```

---

#### Commercial Path (PAID)

1. **Register for OncoKB Account** 👤
   - Go to: https://www.oncokb.org
   - Click "Register"
   - Use **business email** address
   - Complete registration

2. **Navigate to License Page** 📄
   - After registration, go to API/License page
   - Select "Commercial License" option
   - Fill out license request form

3. **Provide Business Information** 📋
   - Be prepared to specify:
     - Company name and size
     - Intended use case (research, clinical, product development)
     - Anticipated annual volume (for clinical use)
     - Geographic regions
     - Expected start date

4. **Contact OncoKB Licensing** 📧
   - Email: `licensing@oncokb.org`
   - Subject: "Commercial License Request for [Your Company]"
   - Include:
     - Your registration information
     - Detailed use case description
     - Company details
     - Contact information for contracting

5. **Review License Terms** 📜
   - OncoKB team will send license agreement
   - Review carefully:
     - Annual fee structure
     - Usage limitations
     - **AI/ML training prohibition** (explicitly not allowed)
     - Attribution requirements
   - Coordinate with legal/procurement team

6. **Execute License Agreement** ✍️
   - Sign agreement
   - Set up payment for annual fee
   - Pricing varies by:
     - Company size
     - Use case
     - Report volume
   - Wait for license activation

7. **Receive API Token** 🔑
   - After license execution and payment
   - API token will be provided
   - Save securely
   - Test access

---

### Estimated Timeline
- **Academic**: 15-30 minutes (immediate after email verification)
- **Commercial**: 1-4 weeks (depends on license negotiation)

### Important Restrictions
- ⚠️ **CANNOT use OncoKB data for AI/ML model training**
- ⚠️ Must cite OncoKB in publications
- ⚠️ Academic users cannot use for commercial purposes

### Notes
- Keep API token secure (treat like a password)
- Tokens don't expire but can be regenerated if compromised
- Rate limits may apply to API (check documentation)

---

## TCGA (via GDC)

### Account/Access Setup
- **Required**: ❌ None (for open access data)
- **Required**: ✅ dbGaP Authorization (for controlled access data)

### Tasks

#### Step 1: Determine Data Access Needs 🔍

**Open Access Data** (No account needed):
- Somatic mutations (MAF files)
- Gene expression data
- Clinical data
- Copy number segments
- DNA methylation (processed)
- Protein expression

**Controlled Access Data** (Authorization needed):
- Raw sequencing (BAM, FASTQ)
- Germline variants
- SNP genotypes
- Individual-level identifying data

---

#### Open Access Path (No Action Required)

1. **No setup required** for:
   - GDC Portal browsing: https://portal.gdc.cancer.gov
   - GDC Data Transfer Tool downloads
   - GDC API queries
   - Open access file downloads

2. **Install GDC Data Transfer Tool** 💻
   - Download from: https://gdc.cancer.gov/access-data/gdc-data-transfer-tool
   - Choose platform: Linux, macOS, or Windows
   - Unzip and add to PATH (optional but recommended):
     ```bash
     # macOS/Linux example
     mv gdc-client /usr/local/bin/
     chmod +x /usr/local/bin/gdc-client
     ```
   - Test installation:
     ```bash
     gdc-client --help
     ```

3. **Start Using** ✅
   - No authentication needed for open access data
   - Generate manifests from GDC Portal
   - Download using:
     ```bash
     gdc-client download -m manifest.txt
     ```

---

#### Controlled Access Path (Required for Raw Sequencing Data)

**Timeline**: Allow 2-6 weeks for complete authorization process

##### Step 1: Create NIH eRA Commons Account 👤

1. **Contact Your Institution's Signing Official (SO)** 📧
   - Every institution has an eRA Commons Signing Official
   - Find yours at: https://era.nih.gov/roster/
   - Email your SO and request eRA Commons account
   - Provide:
     - Full name
     - Email
     - Position/title
     - Reason for access (TCGA data access)

2. **SO Will Create Your Account**
   - SO initiates account creation in eRA Commons
   - You'll receive email notification
   - Follow instructions to set password
   - Log in to verify: https://commons.era.nih.gov/

3. **Complete eRA Commons Profile**
   - Add/verify personal information
   - Add credentials (degrees)
   - Complete all required fields

**Estimated Time**: 1-3 business days

---

##### Step 2: Apply for dbGaP Authorization 📋

1. **Identify Your Role**
   - Are you the **Principal Investigator (PI)** or **Researcher**?
   - If PI: You'll submit the request
   - If Researcher: Your PI must submit request and add you

2. **PI: Submit Data Access Request**
   - Go to: https://dbgap.ncbi.nlm.nih.gov/
   - Click "My Projects" → "Request Access"
   - Search for study: "phs000178" (TCGA)
   - Click "Request Access to Data Sets"

3. **Complete Research Use Statement** 📝
   - Describe your research project:
     - Title
     - Research objectives
     - How TCGA data will be used
     - Expected outcomes
     - Whether publishing results
   - Be specific and detailed
   - Must align with TCGA data use limitations

4. **Fill Out Data Access Request Form** 📄
   - Provide:
     - PI information
     - Institution details
     - Collaborators/researchers who need access
     - IRB information (if applicable)
     - Data security plan
     - Data destruction plan
   - Answer all questions thoroughly

5. **Institutional Certification** ✍️
   - Your institution's Signing Official must:
     - Review your request
     - Certify institutional compliance
     - Sign the request electronically
   - Coordinate with your SO before submitting

6. **Submit Request**
   - Review all information
   - Submit to NIH Data Access Committee (DAC)
   - Request ID will be generated
   - Track status in dbGaP

**Estimated Time to Complete Forms**: 2-4 hours
**Estimated Time for SO Review**: 1-5 business days

---

##### Step 3: Wait for DAC Decision ⏳

1. **NIH Data Access Committee Review**
   - DAC reviews all requests
   - Typically takes 5-10 business days
   - May request additional information
   - Check dbGaP portal for status updates

2. **Respond to Any Requests**
   - If DAC requests clarification, respond promptly
   - Delays in response extend timeline

3. **Receive Decision**
   - Email notification sent to PI
   - Approval or rejection with reasoning
   - If approved: Authorization period (typically 1 year)
   - Must renew annually

**Estimated Time**: 5-10 business days (can be longer)

---

##### Step 4: Download Authentication Token 🔑

1. **Access GDC Portal After Approval**
   - Log in to: https://portal.gdc.cancer.gov
   - Click on your name/account
   - Navigate to "Download Token"

2. **Generate Token**
   - Click "Generate Token"
   - Token file downloads automatically: `gdc-user-token.txt`
   - **SAVE THIS FILE SECURELY**
   - Token is valid for 30 days (regenerate as needed)

3. **Store Token Safely** 💾
   - Keep in secure location
   - Do not share
   - Do not commit to version control
   - Recommended location: `~/.gdc/token.txt`

**Estimated Time**: 2 minutes

---

##### Step 5: Download Controlled Access Data 📥

1. **Use Token with GDC Data Transfer Tool**
   ```bash
   gdc-client download -m manifest.txt -t gdc-user-token.txt
   ```

2. **Or Use Token with API**
   ```python
   import requests

   token = open('gdc-user-token.txt', 'r').read().strip()
   headers = {'X-Auth-Token': token}

   response = requests.get(
       'https://api.gdc.cancer.gov/data/FILE_UUID',
       headers=headers
   )
   ```

3. **Verify Downloads Work** ✅
   - Test with small file first
   - Confirm authentication is working
   - Check data integrity (MD5 checksums)

---

### Data Use Compliance ⚖️

Once you have controlled access:

1. **Follow Data Use Limitations**
   - Use only for approved research
   - Do NOT attempt to identify individuals
   - Keep data secure
   - Destroy data when research complete

2. **Manage Team Access**
   - Only approved individuals can access
   - Add collaborators through dbGaP if needed
   - Document who has access

3. **Renewal** 🔄
   - Authorization expires after 1 year
   - Renew before expiration
   - Update research use statement if changed
   - Process is faster than initial request

---

### Estimated Total Timeline

| Path | Minimum Time | Typical Time | Maximum Time |
|------|-------------|--------------|--------------|
| **Open Access** | Immediate | Immediate | Immediate |
| **Controlled Access** | 2 weeks | 3-4 weeks | 6+ weeks |

### Common Issues and Solutions

**Issue**: eRA Commons account delayed
- **Solution**: Follow up with institutional SO, provide all info upfront

**Issue**: dbGaP request rejected
- **Solution**: Review rejection reason, revise research use statement, resubmit

**Issue**: Token expired
- **Solution**: Regenerate token from GDC portal (takes 2 minutes)

### Notes
- Open access data is completely free and immediate
- Controlled access is free but requires authorization process
- Must have institutional affiliation for dbGaP
- Cannot get controlled access as independent researcher
- Keep tokens secure and regenerate every 30 days

---

## Summary Checklist

Quick reference for what you need to do:

| Data Source | Account Needed? | Commercial License? | Estimated Setup Time |
|-------------|----------------|---------------------|---------------------|
| **cBioPortal** | ❌ No | ❌ No | Immediate |
| **ClinGen** | ❌ No* | ❌ No | Immediate |
| **ClinVar** | ❌ No* | ❌ No | Immediate |
| **COSMIC** | ✅ Yes | ⚠️ If commercial | Academic: 10-30 min<br>Commercial: 1-4 weeks |
| **GenCC** | ❌ No | ❌ No | Immediate |
| **OncoKB** | ✅ Yes | ⚠️ If commercial | Academic: 15-30 min<br>Commercial: 1-4 weeks |
| **TCGA** | ❌ No** | ❌ No | Open: Immediate<br>Controlled: 2-6 weeks |

\* Only if submitting new data
\*\* Only for open access data; controlled access requires dbGaP authorization

---

## Priority Order for Setup

If setting up sequentially, recommended order:

1. **Immediate access** (Start using now):
   - cBioPortal
   - ClinGen
   - ClinVar
   - GenCC
   - TCGA (open access)

2. **Quick setup** (Complete within 1 day):
   - OncoKB (academic) - 15-30 minutes
   - COSMIC (academic) - 10-30 minutes

3. **Longer timeline** (If needed):
   - OncoKB (commercial) - Start ASAP if needed
   - COSMIC (commercial) - Start ASAP if needed
   - TCGA (controlled access) - Start ASAP if needed (longest timeline)

---

## Important Reminders

1. **Save All Credentials Securely**
   - Use password manager
   - Document where tokens/passwords are stored
   - Do not commit to version control

2. **Document Your Accounts**
   - Keep list of usernames, registration emails
   - Note renewal dates (especially TCGA authorization)
   - Track license expiration dates

3. **Test Early**
   - Verify API access works before starting large projects
   - Download small test files first
   - Confirm authentication/authorization

4. **Plan Ahead for Controlled Access**
   - TCGA controlled access takes 2-6 weeks
   - Start process early if you need raw sequencing data
   - Coordinate with institutional officials

5. **Respect License Terms**
   - Don't use academic accounts for commercial purposes
   - Follow AI/ML restrictions (OncoKB)
   - Cite data sources in publications
   - Comply with data use certifications

---

*Last Updated: 2025*
*This document covers setup as of the date above. Check individual source websites for any policy changes.*
